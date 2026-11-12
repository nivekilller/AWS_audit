import boto3
import argparse

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

def main():
    parser = argparse.ArgumentParser(description="AWS Security Auditor MVP")
    parser.add_argument("--local", action="store_true", help="Use LocalStack endpoint")
    args = parser.parse_args()

    endpoint = "http://localhost:4566" if args.local else None

    # Initialize clients
    s3 = boto3.client('s3', endpoint_url=endpoint, aws_access_key_id='test', aws_secret_access_key='test', region_name='us-east-1')

    print("Starting Cloud Security Scan...")
    check_s3_buckets(s3)

if __name__ == "__main__":
    main()