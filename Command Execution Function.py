# command_utils.py

import subprocess

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        # Handle subprocess CalledProcessError
        raise e
