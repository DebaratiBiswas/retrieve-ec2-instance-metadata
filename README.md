# Retrieve-ec2-instance-metadata
This repo is for fetching the metadata of the AWS EC2 instance. The solution is present for both getting all the instance metadata and getting a particular instance metadata based on the key.

# Steps  
Clone the git repo locally   
```bash
git clone https://github.com/DebaratiBiswas/retrieve-ec2-instance-metadata
```
Install the required packages  
```bash  
pip install requirements.txt   
```   
Execute ec2-connect.py   
```bash    
python3 ec2-connect.py   
```
Input required variables such as REGION, INSTANCE_ID, KEY_FILE_PATH and GITHUB_REPO   
REGION = AWS region where ec2 server is present   
INSTANCE_ID  = EC2 instance id   
KEY_FILE_PATH = local path to .pem private key file      
GITHUB_REPO = path to GitHub repository      

Create a client object ec2_client that allows to interact with the Amazon EC2   

**Function start_instances:**   
AWS doc: [AWS SDK python3 boto3](https://docs.aws.amazon.com/code-library/latest/ug/python_3_ec2_code_examples.html)   
Start the EC2 instance: [start instances doc](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/start_instances.html#)   
Wait until the instance is in running state. [InstanceRunning doc](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/waiter/InstanceRunning.html#)  

**Function get_instance_public_ip:**   
Get the public ip of the EC2 instance: [describe instances doc](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_instances.html#)   

**Function execute_commands_via_ssh:**   
Create private key object: [pramiko rsakey doc](https://docs.paramiko.org/en/stable/api/keys.html#module-paramiko.rsakey)    
Create ssh client object to establish connection to ec2 server specifying hostname, user and key. [client doc](https://docs.paramiko.org/en/stable/api/client.html)   
Set of commands to execute within ec2 server to install git, python3 and pip. clone the git repository and install packages mentioned in requirements.txt.  
Check if key for fetching particular instance metadata is specified else print the entire list of instance metadata.    
close ssh connection.   

**ec2-instance-metadata.py:**   
Create a key object if any particular instance metadata key is passed    

**Function get_metadata:**    
[Request doc](https://docs.python-requests.org/en/latest/index.html)   
Request for instance metadata value for the specified key and return the key and value as dict.   
Else Request for list of instance metadata value for ec2 server and return entire keys and values as dict.   
Print the metadata in json format.   




