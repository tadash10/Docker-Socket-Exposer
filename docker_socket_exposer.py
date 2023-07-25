# docker_socket_exposer.py

import subprocess

def expose_socket(container, port):
    try:
        # Get the container ID and port to expose
        container_id = container.id
        port_to_expose = port.split('/')[0]

        # Execute the Docker command to expose the socket
        command = f"docker exec -d {container_id} socat TCP-LISTEN:{port_to_expose},fork,reuseaddr EXEC:'/path/to/your/application'"
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        # Handle subprocess CalledProcessError
        raise e
