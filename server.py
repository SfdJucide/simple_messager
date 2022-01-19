import time
from sys import argv
import select
import json
from socket import AF_INET, SOCK_STREAM, socket

import logging
from log.server_log_config import log


logger = logging.getLogger('server_logger')


@log
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


@log
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
    clients = []
    messages = []

    s = socket(AF_INET, SOCK_STREAM)
    s.bind(parse_argv(argv))
    s.settimeout(0.5)
    s.listen(5)
    logger.info('Сервер готов!')

    while True:
        try:
            client, client_addr = s.accept()
        except:
            pass
        else:
            logger.info(f"Соединение с клиентом {client_addr} установлено")
            clients.append(client)

        recv_data_lst = []
        send_data_lst = []

        try:
            if clients:
                recv_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
        except OSError:
            pass

        if recv_data_lst:
            for client_mess in recv_data_lst:
                try:
                    data = client_mess.recv(100000)
                    json_data = data.decode('utf-8')
                    message = json.loads(json_data)

                    response = get_response(message)
                except:
                    logger.info(f'Клиент {client_mess.getpeername()} отключился от сервера')
                    clients.remove(client_mess)

        if messages and send_data_lst:
            message = {
                'action': 'message',
                'sender': messages[0][0],
                'time': time.time(),
                'text': messages[0][1]
            }
            del message[0]

            for client in send_data_lst:
                try:
                    json_message = json.dumps(response)
                    client.send(json_message.encode('utf-8'))
                except:
                    logger.info(f'Клиент {client.getpeername()} отключился от сервера.')
                    clients.remove(client)


if __name__ == '__main__':
    runserver()
