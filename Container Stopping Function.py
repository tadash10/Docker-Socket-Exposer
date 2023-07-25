# docker_utils.py

def stop_container(container):
    try:
        container.stop()
    except docker.errors.APIError as e:
        # Handle Docker APIError when stopping containers
        raise e
