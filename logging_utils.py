# logging_utils.py

import logging

def configure_logging(log_filename='docker_socket_exposer.log', log_level=logging.INFO):
    logging.basicConfig(filename=log_filename, level=log_level)

def log_error(message):
    logging.error(message)

def log_warning(message):
    logging.warning(message)
