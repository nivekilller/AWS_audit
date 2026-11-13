An AWS audit tool designed to detect common cloud misconfigurations before they reach production

## Features
- S3 Bucket scanner: looks for public buckets
- EC2 Security Group Scanner: Analyzes EC2 security group inbound rules (`IpPermissions`) to 
flag sensitive management ports (e.g., SSH Port 22, RDP Port 3389) exposed to theentire public
 internet (`0.0.0.0/0`).

AWS_audit/
│
├── run_scan.py                # runs seeder + audit pipeline
├── seed_localstack.py         # Populates LocalStack
├── audit.py                   # Main auditor
├── S3_scanner.py              # S3 bucket audit logic
├── security_group_scanner.py  # EC2 Security Group audit logic
└── requirements.txt           # Project dependencies (boto3, botocore, etc.)