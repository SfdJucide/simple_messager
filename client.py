from sys import argv
import sys
import json
import time
import threading
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


@log
def message_receive(sock, username):
    while True:
        data = sock.recv(100000)
        json_data = data.decode('utf-8')
        response = json.loads(json_data)

        if response['action'] == 'message' and response['destination'] == username:
            print(f'Получено сообщение от пользователя {response["sender"]}:\n'
                  f'{response["text"]}')
        else:
            logger.error(f'Получено некорректное сообщение от сервера: {response}')


@log
def build_communication_message(sock, username='guest'):
    receiver = input('Введите получателя > ')
    message = input('Введите сообщение > ')

    response = {
        'action': 'message',
        'sender': username,
        'destination': receiver,
        'time': time.time(),
        'text': message
    }
    logger.info(f'Сформировано сообщение {response}')

    json_message = json.dumps(response)
    sock.send(json_message.encode('utf-8'))
    logger.info(f'Сообщение отослано пользователю {receiver}')


def user_interactive(sock, username):
    print('Команды месенджера:\n'
          'Q - выход\n'
          'M - отправить сообщение')

    while True:
        command = input('Введите команду > ')
        if command == 'M':
            build_communication_message(sock, username)
        elif command == 'Q':
            print("До свидания!")
            logger.info('Клиент завершил сессию')
        else:
            print("Неверная команда!")


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

    client_name = 'guest'

    receiver = threading.Thread(target=message_receive, args=(s, client_name))
    receiver.daemon = True
    receiver.start()
    logger.info(f'Клиент {client_name} online')

    user_interface = threading.Thread(target=user_interactive, args=(s, client_name))
    user_interface.daemon = True
    user_interface.start()


if __name__ == '__main__':
    logger.info('Клиент подключается к серверу...')
    run_client()
