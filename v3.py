#!/usr/bin/env python3

import docker
import subprocess
import logging

# Configure logging
logging.basicConfig(filename='docker_socket_exposer.log', level=logging.INFO)

def get_docker_containers():
    try:
        client = docker.from_env()
        containers = client.containers.list()
        return containers
    except docker.errors.APIError as e:
        logging.exception(f"Failed to retrieve Docker containers: {str(e)}")

def check_exposed_ports(container):
    try:
        if 'HostConfig' in container.attrs and 'PortBindings' in container.attrs['HostConfig']:
            ports = container.attrs['HostConfig']['PortBindings']
            for port in ports:
                if ports[port] is None:
                    # Socket is not exposed, take proper action
                    expose_socket(container, port)
    except KeyError as e:
        logging.exception(f"Failed to retrieve exposed ports for container {container.id}: {str(e)}")

def expose_socket(container, port):
    try:
        # Get the container ID and port to expose
        container_id = container.id
        port_to_expose = port.split('/')[0]

        # Execute the Docker command to expose the socket
        command = f"docker cp /path/to/your/application {container_id}:/path/to/your/application"
        subprocess.run(command, shell=True, check=True)

        command = f"docker exec -d {container_id} socat TCP-LISTEN:{port_to_expose},fork,reuseaddr EXEC:'/path/to/your/application'"
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        logging.exception(f"Failed to expose socket for container {container.id}: {str(e)}")

def main():
    containers = get_docker_containers()

    if containers:
        for container in containers:
            check_exposed_ports(container)
    else:
        logging.warning("No Docker containers found.")

if __name__ == '__main__':
    main()
