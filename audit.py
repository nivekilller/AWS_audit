import argparse
import boto3
import S3_scanner
import seed_localstack
import security_group_scanner

endpoint = "http://localhost:4566"
fake_creds = {
        "aws_access_key_id": "test",
        "aws_secret_access_key": "test",
        "region_name": "us-east-1"
    }

def start_audit():
    # Initialize clients
    s3 = boto3.client('s3', **fake_creds)
    ec2 = boto3.client('ec2', **fake_creds)

    print("Starting Cloud Security Scan...")
    S3_scanner.check_s3_buckets(s3)
    security_group_scanner.check_security_groups(ec2)