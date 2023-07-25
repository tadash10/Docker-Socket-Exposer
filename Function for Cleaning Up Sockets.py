# docker_socket_exposer.py

def clean_up_socket(container, port):
    try:
        container_id = container.id
        port_to_expose = port.split('/')[0]
        command = f"docker exec {container_id} sh -c 'kill $(lsof -t -i:{port_to_expose})'"
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        # Handle subprocess CalledProcessError
        raise e
