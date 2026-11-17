import boto3

def check_iam_policies(iam_client):
    print("\n--- Scanning IAM Policies ---")
    try:
        response = iam_client.list_policies(Scope='Local')
    except Exception as e:
        print(f"[!] Error fetching IAM policies: {e}")
        return

    policies = response.get('Policies', [])
    if not policies:
        print("    No custom IAM policies found.")
        return

    for policy in policies:
        policy_name = policy['PolicyName']
        policy_arn = policy['Arn']
        default_version_id = policy['DefaultVersionId']
        
        try:
            # Fetch the actual JSON body of the policy version
            version_response = iam_client.get_policy_version(
                PolicyArn=policy_arn,
                VersionId=default_version_id
            )
            document = version_response['PolicyVersion']['Document']
            
            # Check statements for dangerous wildcards
            statements = document.get('Statement', [])
            for stmt in statements:
                effect = stmt.get('Effect')
                action = stmt.get('Action')
                resource = stmt.get('Resource')
                
                # The security check: Flag if effect is Allow and actions/resources use wildcards
                if effect == 'Allow' and (action == '*' or resource == '*'):
                    print(f"[!] VULNERABILITY FOUND in IAM Policy '{policy_name}':")
                    print(f"    Overly permissive access detected! Action: {action} | Resource: {resource}\n")
                    
        except Exception as e:
            print(f"[!] Error inspecting policy {policy_name}: {e}")