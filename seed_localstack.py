import boto3
from botocore.exceptions import ClientError

# LocalStack configuration constants
LOCALSTACK_ENDPOINT = "http://localhost:4566"
AWS_REGION = "us-east-1"
FAKE_CREDENTIALS = {
    "aws_access_key_id": "test",
    "aws_secret_access_key": "test",
    "region_name": AWS_REGION
}

def get_client(service_name):
    """Helper function to instantiate boto3 clients pointing to LocalStack."""
    return boto3.client(service_name, endpoint_url=LOCALSTACK_ENDPOINT, **FAKE_CREDENTIALS)

def seed_s3():
    """Creates mock S3 buckets with intentional misconfigurations for testing."""
    print("[*] Seeding S3 Buckets...")
    s3 = get_client('s3')
    
    bucket_name = "insecure-backup-bucket"
    try:
        s3.create_bucket(Bucket=bucket_name)
        print(f"    [+] Created mock bucket: {bucket_name}")
        # Intentionally leaving out Public Access Block so our scanner catches it!
    except ClientError as e:
        print(f"    [!] Note on {bucket_name}: {e.response['Error']['Message']}")

def seed_security_groups():
    """Placeholder for when we add Security Group vulnerability testing."""
    print("[*] Seeding Security Groups... (Ready for future expansion)")
    # ec2 = get_client('ec2')
    # We will write code here soon to open port 22/3389 to 0.0.0.0/0!

def seed_iam():
    """Placeholder for when we add IAM wildcard policy testing."""
    print("[*] Seeding IAM Policies... (Ready for future expansion)")
    # iam = get_client('iam')
    # We will write code here soon to create overly permissive policies!

if __name__ == "__main__":
    print("=== Initializing LocalStack Test Environment ===")
    seed_s3()
    seed_security_groups()
    seed_iam()
    print("=== Seeding Complete! Ready to scan. ===")