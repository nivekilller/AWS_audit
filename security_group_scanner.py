import boto3

# An instance of reponse looks like the following (JSON):
# response = {
#     "SecurityGroups": [
#         {
#             "GroupId": "sg-0123456789abcdef0",
#             "GroupName": "web-server-sg",
#             "Description": "Security group for web servers",
#             "IpPermissions": [
#                 {
#                     "IpProtocol": "tcp",
#                     "FromPort": 22,
#                     "ToPort": 22,
#                     "IpRanges": [
#                         {
#                             "CidrIp": "0.0.0.0/0"
#                         }
#                     ]
#                 }
#             ]
#         }
#     ]
# }

def check_security_groups(ec2_client):
    print("[*] Scanning Security Groups...")
    try:
        response = ec2_client.describe_security_groups()
    except Exception as e:
        print(f"[!] Error fetching security groups: {e}")
        return
    
    for group in response['SecurityGroups']:
        group_name = group.get('GroupName', 'Unknown')
        group_id = group.get('GroupId', 'Unknown')
        
        for permission in group.get('IpPermissions', []):
            from_port = permission.get('FromPort', 0)
            to_port = permission.get('ToPort', 0)
            
            for ip_range in permission.get('IpRanges', []):
                cidr = ip_range.get('CidrIp', '')
                
                # The security check
                # Flag if Port 22 (SSH) or Port 3389 (RDP) is open to the whole world (0.0.0.0/0)
                if cidr == '0.0.0.0/0':
                    if from_port <= 22 <= to_port or from_port <= 3389 <= to_port:
                        print(f"[!] VULNERABILITY FOUND in Security Group '{group_name}' ({group_id}):")
                        print(f"    Port {from_port}-{to_port} is exposed to the public internet ({cidr})!\n")