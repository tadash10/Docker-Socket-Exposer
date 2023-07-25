# main.py

import docker_utils
import docker_ports
import docker_socket_exposer
import logging_utils
import error_handling
import command_utils

def main():
    # Configure logging
    logging_utils.configure_logging()

    # Get Docker containers
    try:
        containers = docker_utils.get_docker_containers()
    except Exception as e:
        error_handling.log_exception(logging, f"Error getting Docker containers: {str(e)}")
        return

    if containers:
        for container in containers:
            try:
                if docker_ports.check_exposed_ports(container):
                    # Stop the container (graceful stop)
                    try:
                        docker_utils.stop_container(container)
                    except Exception as e:
                        error_handling.log_exception(logging, f"Error stopping container {container.id}: {str(e)}")
                        continue

                    # Clean up previously exposed sockets
                    try:
                        docker_socket_exposer.clean_up_socket(container, '8080/tcp')
                    except Exception as e:
                        error_handling.log_exception(logging, f"Error cleaning up socket for container {container.id}: {str(e)}")
                        continue

                    # Start the container if not running
                    try:
                        docker_utils.start_container(container)
                    except Exception as e:
                        error_handling.log_exception(logging, f"Error starting container {container.id}: {str(e)}")
                        continue

                    # Expose socket
                    try:
                        docker_socket_exposer.expose_socket(container, '8080/tcp')
                    except Exception as e:
                        error_handling.log_exception(logging, f"Error exposing socket for container {container.id}: {str(e)}")
            except Exception as e:
                error_handling.log_exception(logging, f"Error processing container {container.id}: {str(e)}")

    else:
        logging_utils.log_warning("No Docker containers found.")

if __name__ == '__main__':
    main()
