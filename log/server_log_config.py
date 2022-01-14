import logging
import inspect

logging.basicConfig(
    filename='server.log',
    format="%(asctime)-20s %(levelname)-10s %(module)-20s %(message)s",
    level=logging.INFO
)

server_log = logging.getLogger('server_logger')


def log(func):
    def call(*args, **kwargs):
        res = func(*args, **kwargs)
        server_log.info(f'Функция: {func.__name__} Параметры: {args}, {kwargs} '
                        f'Вызов из функции {inspect.stack()[1][3]}')
        return res
    return call
