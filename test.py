import boto3
import os
import subprocess
import json
iam_client = boto3.client('iam')

def list_user_cli():
    list_cmd = "aws iam list-users"
    output = subprocess.check_output(list_cmd, shell = True)
    output = str(output.decode('ascii'))
    return output

def write_json_file(filename, data):
    try:
        with open(filename, "w") as f:
            f.writelines(data)
        print(filename + " has been created.")
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    filename = "iam.json"
    data = list_user_cli()
    write_json_file(filename, data)
