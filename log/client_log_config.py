import logging


logging.basicConfig(
    filename='client.log',
    format="%(asctime)-20s %(levelname)-10s %(module)-20s %(message)s",
    level=logging.INFO
)

client_log = logging.getLogger('client_logger')
