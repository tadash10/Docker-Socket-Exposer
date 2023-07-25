# docker_ports.py

def check_exposed_ports(container):
    try:
        if 'HostConfig' in container.attrs and 'PortBindings' in container.attrs['HostConfig']:
            ports = container.attrs['HostConfig']['PortBindings']
            for port in ports:
                if ports[port] is None:
                    # Socket is not exposed, take proper action
                    return True
    except KeyError as e:
        # Handle KeyError
        raise e
    return False
