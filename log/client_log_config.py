import logging
import inspect

from core.settings import LOGGING_LEVEL


logging.basicConfig(
    filename='log/client.log',
    format="%(asctime)-20s %(levelname)-10s %(module)-20s %(message)s",
    level=LOGGING_LEVEL
)

client_log = logging.getLogger('client_logger')


def log(func):
    def call(*args, **kwargs):
        res = func(*args, **kwargs)
        client_log.info(f'Функция: {func.__name__} Параметры: {args}, {kwargs} '
                        f'Вызов из функции {inspect.stack()[1][3]}')
        return res
    return call
