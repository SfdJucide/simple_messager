from sys import argv
import sys
import json
import time
import threading
from socket import socket, AF_INET, SOCK_STREAM

import logging
from log.client_log_config import log


class ClientVerifier(type):
    pass


class Client(metaclass=ClientVerifier):

    def __init__(self):
        self.args = argv
        self.sock = socket(AF_INET, SOCK_STREAM)

    @log
    def build_presence_message(self, user='Guest'):
        presence_message = {
            'action': 'presence',
            'time': time.time(),
            'user': user
        }
        logger.info('Сообщение серверу сформировано: %s', presence_message)
        return presence_message

    @log
    def parse_client_argv(self):
        try:
            addr = self.args[1]
            port = int(self.args[2])
        except IndexError:
            logger.warning('Неверно переданы адресс или порт')
            addr = 'localhost'
            port = 7777

        return addr, port

    @log
    def check_server_answer(self, response):
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

    # @staticmethod
    # def get_message(sock, username):
    #     input('Для выхода нажмите Q')
    #     message = input('Введите сообщение: ')
    #     if message == 'Q':
    #         sock.close()
    #         logger.info('Завершение сессии...')
    #         sys.exit(0)
    #     message_context = {
    #         'action': 'message',
    #         'time': time.time(),
    #         'username': username,
    #         'text': message
    #     }
    #     logger.info(f'Сформировано сообщение: {message_context}')
    #     return message_context

    @log
    def message_receive(self, sock, username):
        while True:
            data = sock.recv(100000)
            json_data = data.decode('utf-8')
            response = json.loads(json_data)

            if response['action'] == 'message' and response['destination'] == username:
                print(f'\nПолучено сообщение от пользователя {response["sender"]}:\n'
                      f'{response["text"]}')
            else:
                logger.warning(f'Получено некорректное сообщение от сервера: {response}')

    @log
    def build_communication_message(self, sock, username='guest'):
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

    def user_interactive(self, sock, username):
        print('Команды месенджера:\n'
              'Q - выход\n'
              'M - отправить сообщение')

        while True:
            command = input('Введите команду > ')
            if command == 'M':
                self.build_communication_message(sock, username)
            elif command == 'Q':
                print("До свидания!")
                sock.close()
                logger.info('Клиент завершил сессию')
                sys.exit(0)
            else:
                print("Неверная команда!")

    def run_client(self):
        addr, port = self.parse_client_argv()
        self.sock.connect((addr, port))
        client_name = input('Введите ваш ник > ')

        # message = self.build_presence_message()
        # json_message = json.dumps(message)
        # self.sock.send(json_message.encode('utf-8'))
        #
        # data = self.sock.recv(100000)
        # json_data = data.decode('utf-8')
        # response = json.loads(json_data)
        #
        # self.check_server_answer(response)

        receiver = threading.Thread(target=self.message_receive, args=(self.sock, client_name))
        receiver.daemon = True
        receiver.start()

        user_interface = threading.Thread(target=self.user_interactive, args=(self.sock, client_name))
        user_interface.daemon = True
        user_interface.start()

        logger.info(f'Клиент {client_name} online')

        receiver.join()
        user_interface.join()


if __name__ == '__main__':
    logger = logging.getLogger('client_logger')
    logger.info('Клиент подключается к серверу...')
    client = Client()
    client.run_client()
