from sys import argv
import sys
import json
import time
from socket import socket, AF_INET, SOCK_STREAM

import logging
from log.client_log_config import log


logger = logging.getLogger('client_logger')


@log
def build_message(user):
    presence_message = {
        'action': 'presence',
        'time': time.time(),
        'user': user
    }
    logger.info('Сообщение серверу сформировано: %s', presence_message)
    return presence_message


@log
def parse_client_argv(args):
    try:
        addr = args[1]
        port = int(args[2])
        mode = args[3]
    except IndexError:
        logger.warning('Неверно переданы адресс или порт')
        addr = 'localhost'
        port = 7777
        mode = 'listen'

    if mode not in ('listen', 'send'):
        logger.error('Указан неверный режим работы клиента!')

    return addr, port, mode


@log
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


def get_message(sock, username):
    input('Для выхода нажмите Q')
    message = input('Введите сообщение: ')
    if message == 'Q':
        sock.close()
        logger.info('Завершение сессии...')
        sys.exit(0)
    message_context = {
        'action': 'message',
        'time': time.time(),
        'username': username,
        'text': message
    }
    logger.info(f'Сформировано сообщение: {message_context}')
    return message_context


def run_client():
    s = socket(AF_INET, SOCK_STREAM)
    addr, port, mode = parse_client_argv(argv)
    s.connect((addr, port))

    message = build_message('guest')
    json_message = json.dumps(message)
    s.send(json_message.encode('utf-8'))

    data = s.recv(100000)
    json_data = data.decode('utf-8')
    response = json.loads(json_data)

    check_server_answer(response)

    if mode == 'send':
        print('Режим работы - отправка сообщений.')
    else:
        print('Режим работы - приём сообщений.')

    while True:
        if mode == 'send':
            try:
                message = get_message(s, 'guest')
                json_message = json.dumps(message)
                s.send(json_message.encode('utf-8'))

            except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                logger.error(f'Соединение с сервером {addr} было потеряно.')
                sys.exit(1)

        if mode == 'listen':
            try:
                data = s.recv(100000)
                json_data = data.decode('utf-8')
                response = json.loads(json_data)

                check_server_answer(response)
            except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                logger.error(f'Соединение с сервером {addr} было потеряно.')
                sys.exit(1)


if __name__ == '__main__':
    logger.info('Клиент подключается к серверу...')
    run_client()
