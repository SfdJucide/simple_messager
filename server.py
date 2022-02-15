import time
from sys import argv
import select
import json
from socket import AF_INET, SOCK_STREAM, socket

import logging
from log.server_log_config import log


class CheckPort:
    def __init__(self):
        self.port = 7777

    def __get__(self, instance, instance_type):
        return self.port

    def __set__(self, instance, value):
        if isinstance(value, int) and value >= 0:
            self.port = value
        else:
            raise ValueError("Неверно указан порт!")


class ServerVerifier(type):
    pass


class Server(metaclass=ServerVerifier):

    def __init__(self):
        self.args = argv
        self.clients = []
        self.messages = []
        self.sock = socket(AF_INET, SOCK_STREAM)

    @log
    def parse_argv(self):
        try:
            cp = CheckPort
            cp.port = int(self.args[self.args.index('-p') + 1])
            # if '-p' in self.args:
            #     port = int(self.args[self.args.index('-p') + 1])
            # else:
            #     port = 7777

            if '-a' in self.args:
                addr = self.args[self.args.index('-a') + 1]
            else:
                addr = ''

            logger.info('Получены адрес и порт для сервера')
            return addr, cp.port
        except ValueError:
            logger.error('Неверно переданы аргументы командной строки!')

    @log
    def get_response(self, message, message_list, client):
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
            message_list.append(response)
        except KeyError:
            logger.error('Неправильно сформирован ответ клиента!')

    def runserver(self):
        addr, port = self.parse_argv()
        self.sock.bind((addr, port))
        self.sock.listen(5)
        self.sock.settimeout(0.5)
        logger.info(f'Сервер запущен по адресу {addr}:{port}')

        while True:
            try:
                client, client_addr = self.sock.accept()
            except:
                pass
            else:
                logger.info(f"Соединение с клиентом {client_addr} установлено")
                self.clients.append(client)
                logger.info(f"список клиентов: {self.clients}")

            recv_data_lst = []
            send_data_lst = []

            try:
                if self.clients:
                    recv_data_lst, send_data_lst, err_lst = select.select(self.clients, self.clients, [], 0)
            except OSError:
                pass

            if recv_data_lst:
                for client_mess in recv_data_lst:
                    try:
                        data = client_mess.recv(100000)
                        json_data = data.decode('utf-8')
                        message = json.loads(json_data)

                        logger.info(f'сообщение принято от {message["sender"]} {message}')

                        response = [message['sender'], message['text'], message['destination']]
                        self.messages.append(response)

                        # self.get_response(message, self.messages, client_mess)
                    except:
                        logger.info(f'Клиент {client_mess.getpeername()} отключился от сервера')
                        self.clients.remove(client_mess)

            if self.messages and send_data_lst:
                logger.info(f'сообщения: {self.messages}')
                message = {
                    'action': 'message',
                    'sender': self.messages[0][0],
                    'time': time.time(),
                    'text': self.messages[0][1],
                    'destination': self.messages[0][2]
                }
                del self.messages[0]

                for client in send_data_lst:
                    try:
                        json_message = json.dumps(message)
                        client.send(json_message.encode('utf-8'))
                    except:
                        logger.info(f'Клиент {client.getpeername()} отключился от сервера.')
                        self.clients.remove(client)


if __name__ == '__main__':
    logger = logging.getLogger('server_logger')
    server = Server()
    server.runserver()
