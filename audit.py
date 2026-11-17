import boto3
import S3_scanner
import security_group_scanner
import iam_policies_scanner

def start_audit():
    s3 = boto3.client('s3')
    ec2 = boto3.client('ec2')
    iam = boto3.client('iam')

    print("Starting Cloud Security Scan...")
    S3_scanner.check_s3_buckets(s3)
    security_group_scanner.check_security_groups(ec2)
    iam_policies_scanner.check_iam_policies(iam)