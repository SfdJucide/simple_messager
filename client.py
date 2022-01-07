from sys import argv
import json
import time
from socket import socket, AF_INET, SOCK_STREAM

import logging
from log import client_log_config


logger = logging.getLogger('client_logger')


def build_message(user):
    presence_message = {
        'action': 'presence',
        'time': time.time(),
        'user': user
    }
    logger.info('Сообщение серверу сформировано: %s', presence_message)
    return presence_message


def parse_client_argv(args):
    try:
        addr = args[1]
        port = int(args[2])
    except IndexError:
        logger.warning('Неверно переданы адресс или порт')
        addr = 'localhost'
        port = 7777

    return addr, port


def check_server_answer(response):
    try:
        if response['response'] == 200:
            h_response = '200: OK'
            logger.info('Ответ сервера: %s', h_response)
        else:
            h_response = '400: Bad Request'
            logger.error('Ответ сервера: %s', h_response)

        return h_response
    except (KeyError, TypeError):
        logger.error('Ошибка ответа сервера')


def run_client():
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(parse_client_argv(argv))
    message = build_message('guest')
    json_message = json.dumps(message)
    s.send(json_message.encode('utf-8'))

    data = s.recv(100000)
    json_data = data.decode('utf-8')
    response = json.loads(json_data)

    check_server_answer(response)


if __name__ == '__main__':
    logger.info('Клиент подключается к серверу...')
    run_client()
