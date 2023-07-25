# docker_utils.py

def start_container(container):
    try:
        if not container.status == 'running':
            container.start()
    except docker.errors.APIError as e:
        # Handle Docker APIError when starting containers
        raise e
