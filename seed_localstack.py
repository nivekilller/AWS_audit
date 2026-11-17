import boto3
from botocore.exceptions import ClientError
import json

# LocalStack configuration constants
LOCALSTACK_ENDPOINT = "http://localhost:4566"
AWS_REGION = "us-east-1"

def get_client(service_name):
    #Helper function to instantiate boto3 clients pointing to LocalStack."""
    return boto3.client(service_name)

def seed_s3():
    #Creates mock S3 buckets with intentional misconfigurations for testing."""
    print("[*] Seeding S3 Buckets...")
    s3 = get_client('s3')
    
    bucket_name = "insecure-backup-bucket"
    try:
        s3.create_bucket(Bucket=bucket_name)
        print(f"    [+] Created mock bucket: {bucket_name}")
        #Intentionally leaving out Public Access Block
    except ClientError as e:
        print(f"    [!] Note on {bucket_name}: {e.response['Error']['Message']}")


def seed_security_groups():
    print("[*] Seeding Security Groups...")
    ec2 = get_client('ec2')
    
    group_name = "insecure-production-sg"
    try:
        response = ec2.create_security_group(
            GroupName=group_name,
            Description='insecure security group'
        )
        group_id = response['GroupId']
        print(f"    [+] Created Security Group: {group_name} ({group_id})")
        
        ec2.authorize_security_group_ingress(
            GroupId=group_id,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 22,
                    'ToPort': 22,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                }
            ]
        )
        print(f"    [+] Added dangerous inbound rule (Port 22 -> 0.0.0.0/0) to {group_name}")
        
    except ClientError as e:
        print(f"    [!] Note on Security Group seeding: {e.response['Error']['Message']}")



def seed_iam():
    print("[*] Seeding IAM Policies...")
    iam = get_client('iam')
    
    policy_name = "InsecureAdminPolicy"
    
    # Define a dangerous wildcard policy
    insecure_policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "*",
                "Resource": "*"
            }
        ]
    }
    
    try:
        # Create the customer-managed policy in LocalStack
        response = iam.create_policy(
            PolicyName=policy_name,
            PolicyDocument=json.dumps(insecure_policy_document),
            Description="A dangerous administrative policy with wildcards for testing"
        )
        print(f"    [+] Created insecure IAM Policy: {policy_name}")
    except ClientError as e:
        print(f"    [!] Note on IAM policy seeding: {e.response['Error']['Message']}")


def run_seeding():
    print("=== Initializing LocalStack Test Environment ===")
    seed_s3()
    seed_security_groups()
    seed_iam()
    print("=== Seeding Complete! Ready to scan. ===")