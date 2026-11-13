import boto3

def check_s3_buckets(s3_client):
    print("\n--- Scanning S3 Buckets ---")
    buckets = s3_client.list_buckets().get('Buckets', [])
    for b in buckets:
        name = b['Name']
        try:
            status = s3_client.get_public_access_block(Bucket=name)
            config = status['PublicAccessBlockConfiguration']
            if not all([config.get('BlockPublicAcls'), config.get('BlockPublicPolicy')]):
                print(f"[!] Warning: Bucket '{name}' public access block is disabled!")
            else:
                print(f"[+] Bucket '{name}' is securely blocked.")
        except s3_client.exceptions.ClientError:
            print(f"[!] Warning: Bucket '{name}' has NO Public Access Block configured!")