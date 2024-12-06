import boto3
import paramiko
import time

# Configuration
REGION = input("Enter your AWS region (e.g., us-east-1): ")
INSTANCE_ID = input("Enter your EC2 instance ID: ")
KEY_FILE_PATH = input("Enter the path to your private key file (e.g., /path/to/your-key.pem): ")
GITHUB_REPO = input("Enter the GitHub repository URL (e.g., https://github.com/your-username/your-repo.git): ")
SCRIPT_TO_RUN = "ec2-instance-metadata.py"
SPECIFIC_KEY = input("Enter a specific metadata key to query (e.g, ami-id or press Enter to fetch all): ")
REMOTE_USER = "ec2-user"  # Default user for Amazon Linux

# Step 1: Start EC2 Instance
# Create client object to interact with the Amazon EC2
ec2_client = boto3.client("ec2", region_name=REGION)
print(f"ec2_client = {ec2_client}")

def start_instance(instance_id):
    print("Starting instance...")
    ec2_client.start_instances(InstanceIds=[instance_id])
    waiter = ec2_client.get_waiter("instance_running")
    waiter.wait(InstanceIds=[instance_id])
    print("Instance is running.")

# Step 2: Get Public IP of EC2 Instance
def get_instance_public_ip(instance_id):
    response = ec2_client.describe_instances(InstanceIds=[instance_id])
    public_ip = response["Reservations"][0]["Instances"][0].get("PublicIpAddress")
    return public_ip

# Step 3: Execute Commands via SSH
def execute_commands_via_ssh(public_ip, key_file):
    print(f"Connecting to EC2 instance at {public_ip}...")

    # Load private key
    key = paramiko.RSAKey.from_private_key_file(key_file)

    # SSH Client setup
    ssh = paramiko.SSHClient()
    ssh.connect(hostname=public_ip, username=REMOTE_USER, pkey=key)
    print("Connected successfully!")

    # Commands to execute
    commands = [
        "sudo yum update -y",
        "sudo yum install git -y",
        "sudo yum install python3 -y",
        "sudo yum install python3-pip -y",
        f"git clone {GITHUB_REPO}",
        f"cd {GITHUB_REPO.split('/')[-1].replace('.git', '')} && pip3 install -r requirements.txt ",
    ]
    if SPECIFIC_KEY:  # If a specific key is provided
        commands.append(f"python3 {SCRIPT_TO_RUN} {SPECIFIC_KEY}")
    else:  # Fetch all metadata
        commands.append(f"python3 {SCRIPT_TO_RUN}")
    # Execute commands
    for command in commands:
        print(f"Executing: {command}")
        stdin, stdout, stderr = ssh.exec_command(command)
        print(stdout.read().decode())
        print(stderr.read().decode())

    # Close SSH connection
    ssh.close()
    print("SSH connection closed.")

# Main
try:
    start_instance(INSTANCE_ID)
    time.sleep(10)  # Give some time for instance initialization
    public_ip = get_instance_public_ip(INSTANCE_ID)
    execute_commands_via_ssh(public_ip, KEY_FILE_PATH)
except Exception as e:
    print(f"Error: {e}")

