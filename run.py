import subprocess
import os
from dotenv import load_dotenv
load_dotenv()

class ProwlerExec:
    def aws_setup(self):
        # AWS credentials
        access_key_id=os.getenv("AWS_ACCESS_KEY")
        secret_access_key=os.getenv("AWS_SECRET_KEY")
        # Command to run aws configure
        aws_configure_command = f'aws configure set aws_access_key_id {access_key_id} && aws configure set aws_secret_access_key {secret_access_key}'

        # Execute the AWS configure command
        aws_configure_process = subprocess.Popen(aws_configure_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        aws_configure_stdout, aws_configure_stderr = aws_configure_process.communicate()

        # Check if the AWS configure command was successful
        if aws_configure_process.returncode == 0:
            print("AWS configure command executed successfully.")
        else:
            print("Failed to execute AWS configure command.")
            print("Error message:", aws_configure_stderr.decode())
            exit(1)

    def prowler_setup(self):
        # Prowler command
        prowler_command = 'prowler -M json csv html'

        # Execute the Prowler command and capture the output and error streams asynchronously
        prowler_process = subprocess.Popen(prowler_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

        # Read output and error streams line by line and print them
        for stdout_line in iter(prowler_process.stdout.readline, b''):
            print(stdout_line.decode(), end='')

        for stderr_line in iter(prowler_process.stderr.readline, b''):
            print(stderr_line.decode(), end='')

        # Wait for the Prowler command to finish
        prowler_process.wait()

        # Check if the Prowler command was successful
        if prowler_process.returncode == 0:
            print("Command '{}' executed successfully.".format(prowler_command))
        else:
            print("Command '{}' failed.".format(prowler_command))

prowler = ProwlerExec()
prowler.aws_setup()
prowler.prowler_setup()