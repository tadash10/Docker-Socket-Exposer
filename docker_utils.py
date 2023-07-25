# docker_utils.py

import docker

def get_docker_containers():
    try:
        client = docker.from_env()
        containers = client.containers.list()
        return containers
    except docker.errors.APIError as e:
        # Handle Docker APIError
        raise e
