from sys import argv
import json
from socket import AF_INET, SOCK_STREAM, socket

import logging
from log import server_log_config


logger = logging.getLogger('server_logger')


def parse_argv(args):
    try:
        if '-p' in args:
            port = int(args[args.index('-p') + 1])
        else:
            port = 7777

        if '-a' in args:
            addr = args[args.index('-a') + 1]
        else:
            addr = ''

        logger.info('Получены адрес и порт для сервера')
        return addr, port
    except ValueError:
        logger.error('Неверно переданы аргументы командной строки!')


def get_response(message):
    try:
        if message['action'] == 'presence' and message['user'] == 'guest':
            response = {
                'response': 200
            }
        else:
            response = {
                'response': 400,
                'error': 'Bad Request'
            }
        logger.info('Сформирован ответ сервера: %s', response)
        return response

    except KeyError:
        logger.error('Неправильно сформирован ответ клиента!')


def runserver():

    s = socket(AF_INET, SOCK_STREAM)
    s.bind(parse_argv(argv))
    s.listen()
    logger.info('Сервер готов!')

    while True:
        client, client_addr = s.accept()
        data = client.recv(100000)
        json_data = data.decode('utf-8')
        message = json.loads(json_data)

        response = get_response(message)

        json_message = json.dumps(response)
        client.send(json_message.encode('utf-8'))
        client.close()


if __name__ == '__main__':
    runserver()
