import seed_localstack
import audit

def run_workflow():
    print("Seeding LocalStack")
    seed_localstack.run_seeding()

    print("Running Security Auditor")
    audit.start_audit()

if __name__ == "__main__":
    run_workflow()