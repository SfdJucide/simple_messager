import logging

logging.basicConfig(
    filename='server.log',
    format="%(asctime)-20s %(levelname)-10s %(module)-20s %(message)s",
    level=logging.INFO
)

server_log = logging.getLogger('server_logger')
