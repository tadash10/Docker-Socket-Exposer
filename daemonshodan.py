import docker
import subprocess
import logging
import shodan

# Configure logging
logging.basicConfig(filename='docker_socket_exposer.log', level=logging.INFO)

# Configure Shodan API key
SHODAN_API_KEY = 'your_shodan_api_key'

def get_docker_containers():
    try:
        client = docker.from_env()
        containers = client.containers.list()
        return containers
    except docker.errors.APIError as e:
        logging.error(f"Failed to retrieve Docker containers: {str(e)}")

def check_exposed_ports(container):
    try:
        ports = container.attrs['HostConfig']['PortBindings']
        if ports:
            for port in ports:
                if ports[port] is None:
                    # Socket is not exposed, take proper action
                    expose_socket(container, port)
                    alert_action(container, port)
    except KeyError as e:
        logging.error(f"Failed to retrieve exposed ports for container {container.id}: {str(e)}")

def expose_socket(container, port):
    try:
        # Get the container ID and port to expose
        container_id = container.id
        port_to_expose = port.split('/')[0]

        # Execute the Docker command to expose the socket
        command = f"docker exec -d {container_id} socat TCP-LISTEN:{port_to_expose},fork,reuseaddr EXEC:'/path/to/your/application'"
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to expose socket for container {container.id}: {str(e)}")

def alert_action(container, port):
    try:
        # Send an alert or notification about the action taken
        alert_message = f"Exposed socket detected in container {container.id}. Port: {port}"
        # Implement your alerting mechanism here (e.g., sending an email, generating a ticket, etc.)
        logging.info(alert_message)
    except Exception as e:
        logging.error(f"Failed to send alert for container {container.id}: {str(e)}")

def search_shodan(query):
    try:
        api = shodan.Shodan(SHODAN_API_KEY)
        results = api.search(query)
        return results
    except shodan.APIError as e:
        logging.error(f"Shodan API error: {str(e)}")

def main():
    containers = get_docker_containers()

    if containers:
        for container in containers:
            check_exposed_ports(container)
    else:
        logging.warning("No Docker containers found.")

    # Search Shodan for exposed Docker sockets
    query = 'docker port:"2375"'
    shodan_results = search_shodan(query)

    if shodan_results:
        for result in shodan_results['matches']:
            # Perform actions for exposed sockets found through Shodan
            container_id = result['ip_str']
            port = result['port']
            # Find the corresponding Docker container and take action
            for container in containers:
                if container_id in container.attrs['NetworkSettings']['Networks']:
                    expose_socket(container, port)
                    alert_action(container, port)
    else:
        logging.info("No exposed Docker sockets found through Shodan.")

if __name__ == '__main__':
    main()
