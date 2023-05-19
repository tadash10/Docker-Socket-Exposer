import docker
import subprocess

def get_docker_containers():
    client = docker.from_env()
    containers = client.containers.list()
    return containers

def check_exposed_ports(container):
    ports = container.attrs['HostConfig']['PortBindings']
    if ports:
        for port in ports:
            if ports[port] is None:
                # Socket is not exposed, take proper action
                expose_socket(container, port)

def expose_socket(container, port):
    # Get the container ID and port to expose
    container_id = container.id
    port_to_expose = port.split('/')[0]

    # Execute the Docker command to expose the socket
    command = f"docker exec -d {container_id} socat TCP-LISTEN:{port_to_expose},fork,reuseaddr EXEC:'/path/to/your/application'"
    subprocess.run(command, shell=True)

def main():
    containers = get_docker_containers()

    for container in containers:
        check_exposed_ports(container)

if __name__ == '__main__':
    main()

