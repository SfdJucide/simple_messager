# from sys import argv
# import sys
# import json
# import time
# import threading
# from socket import socket, AF_INET, SOCK_STREAM
#
# import logging
# from log.client_log_config import log
#
#
# class ClientVerifier(type):
#     pass
#
#
# class Client(metaclass=ClientVerifier):
#
#     def __init__(self):
#         self.args = argv
#         self.sock = socket(AF_INET, SOCK_STREAM)
#         self.login = ''
#
#     @log
#     def build_presence_message(self, user='Guest'):
#         presence_message = {
#             'action': 'presence',
#             'time': time.time(),
#             'user': user
#         }
#         logger.info('Сообщение серверу сформировано: %s', presence_message)
#         return presence_message
#
#     @log
#     def parse_client_argv(self):
#         try:
#             addr = self.args[1]
#             port = int(self.args[2])
#         except IndexError:
#             logger.warning('Неверно переданы адресс или порт')
#             addr = 'localhost'
#             port = 7777
#
#         return addr, port
#
#     @log
#     def check_server_answer(self, response):
#         try:
#             if response['response'] == 200:
#                 h_response = '200: OK'
#                 logger.info('Ответ сервера: %s', h_response)
#             else:
#                 h_response = '400: Bad Request'
#                 logger.error('Ответ сервера: %s', h_response)
#
#             return h_response
#         except (KeyError, TypeError):
#             logger.error('Ошибка ответа сервера')
#
#     # @staticmethod
#     # def get_message(sock, username):
#     #     input('Для выхода нажмите Q')
#     #     message = input('Введите сообщение: ')
#     #     if message == 'Q':
#     #         sock.close()
#     #         logger.info('Завершение сессии...')
#     #         sys.exit(0)
#     #     message_context = {
#     #         'action': 'message',
#     #         'time': time.time(),
#     #         'username': username,
#     #         'text': message
#     #     }
#     #     logger.info(f'Сформировано сообщение: {message_context}')
#     #     return message_context
#
#     @log
#     def message_receive(self, sock, username):
#         while True:
#             data = sock.recv(100000)
#             json_data = data.decode('utf-8')
#             response = json.loads(json_data)
#
#             if response['action'] == 'message' and response['destination'] == username:
#                 print(f'\nПолучено сообщение от пользователя {response["sender"]}:\n'
#                       f'{response["text"]}')
#             else:
#                 logger.warning(f'Получено некорректное сообщение от сервера: {response}')
#
#     @log
#     def manage_contacts(self, sock, func):
#         if func == 1:
#             response = {
#                 "action": "get_contacts",
#                 "time": time.time(),
#                 "user_login": self.login
#             }
#         elif func == 2:
#             username_to_add = input("Введите логин пользователя > ")
#             response = {
#                 "action": "add_contact",
#                 "time": time.time(),
#                 "user_login": self.login,
#                 "user_id": username_to_add
#             }
#         elif func == 3:
#             username_to_del = input("Введите логин пользователя > ")
#             response = {
#                 "action": "del_contact",
#                 "time": time.time(),
#                 "user_login": self.login,
#                 "user_id": username_to_del
#             }
#         else:
#             print("Неизвестная команда")
#
#         logger.info(f'Сформировано сообщение {response}')
#
#         json_message = json.dumps(response)
#         sock.send(json_message.encode('utf-8'))
#
#
#     @log
#     def build_communication_message(self, sock, username='guest'):
#         receiver = input('Введите получателя > ')
#         message = input('Введите сообщение > ')
#
#         response = {
#             'action': 'message',
#             'sender': username,
#             'destination': receiver,
#             'time': time.time(),
#             'text': message
#         }
#         logger.info(f'Сформировано сообщение {response}')
#
#         json_message = json.dumps(response)
#         sock.send(json_message.encode('utf-8'))
#
#         logger.info(f'Сообщение отослано пользователю {receiver}')
#
#     def user_interactive(self, sock, username):
#         print('Команды месенджера:\n'
#               'Q - выход\n'
#               'M - отправить сообщение\n'
#               'K - управление контактами')
#
#         while True:
#             command = input('Введите команду > ')
#             if command == 'M':
#                 self.build_communication_message(sock, username)
#             elif command == 'Q':
#                 print("До свидания!")
#                 sock.close()
#                 logger.info('Клиент завершил сессию')
#                 sys.exit(0)
#             elif command == 'K':
#                 print('Посмотреть список контактов -> 1\n'
#                       'Добавить контакт -> 2\n'
#                       'Удалить контакт -> 3')
#                 func = int(input('Введите команду > '))
#                 self.manage_contacts(sock, func)
#             else:
#                 print("Неверная команда!")
#
#     def run_client(self):
#         addr, port = self.parse_client_argv()
#         self.sock.connect((addr, port))
#         self.login = input('Введите ваш ник > ')
#
#         # message = self.build_presence_message()
#         # json_message = json.dumps(message)
#         # self.sock.send(json_message.encode('utf-8'))
#         #
#         # data = self.sock.recv(100000)
#         # json_data = data.decode('utf-8')
#         # response = json.loads(json_data)
#         #
#         # self.check_server_answer(response)
#
#         receiver = threading.Thread(target=self.message_receive, args=(self.sock, self.login))
#         receiver.daemon = True
#         receiver.start()
#
#         user_interface = threading.Thread(target=self.user_interactive, args=(self.sock, self.login))
#         user_interface.daemon = True
#         user_interface.start()
#
#         logger.info(f'Клиент {self.login} online')
#
#         receiver.join()
#         user_interface.join()
#
#
# if __name__ == '__main__':
#     logger = logging.getLogger('client_logger')
#     logger.info('Клиент подключается к серверу...')
#     client = Client()
#     client.run_client()

import sys
import json
import socket
import time
import argparse
import threading

from log.client_log_config import log
from core.settings import *
from commons.utils import send_message, get_message
from commons.errors import IncorrectDataRecivedError, ReqFieldMissingError, ServerError

# Инициализация клиентского логера
logger = logging.getLogger('client')


# Функция создаёт словарь с сообщением о выходе.
@log
def create_exit_message(account_name):
    return {
        ACTION: EXIT,
        TIME: time.time(),
        ACCOUNT_NAME: account_name
    }


@log
# Функция - обработчик сообщений других пользователей, поступающих с сервера.
def message_from_server(sock, my_username):
    while True:
        try:
            message = get_message(sock)
            if ACTION in message and message[ACTION] == MESSAGE and SENDER in message and DESTINATION in message \
                    and MESSAGE_TEXT in message and message[DESTINATION] == my_username:
                print(f'\nПолучено сообщение от пользователя {message[SENDER]}:\n{message[MESSAGE_TEXT]}')
                logger.info(f'Получено сообщение от пользователя {message[SENDER]}: {message[MESSAGE_TEXT]}')
            else:
                logger.error(f'Получено некорректное сообщение с сервера: {message}')
        except IncorrectDataRecivedError:
            logger.error(f'Не удалось декодировать полученное сообщение.')
        except (OSError, ConnectionError, ConnectionAbortedError, ConnectionResetError, json.JSONDecodeError):
            logger.critical(f'Потеряно соединение с сервером.')
            break


@log
# Функция запрашивает кому отправить сообщение и само сообщение, и отправляет полученные данные на сервер.
def create_message(sock, account_name='Guest'):
    to = input('Введите получателя сообщения: ')
    message = input('Введите сообщение для отправки: ')
    message_dict = {
        ACTION: MESSAGE,
        SENDER: account_name,
        DESTINATION: to,
        TIME: time.time(),
        MESSAGE_TEXT: message
    }
    logger.debug(f'Сформирован словарь сообщения: {message_dict}')
    try:
        send_message(sock, message_dict)
        logger.info(f'Отправлено сообщение для пользователя {to}')
    except:
        logger.critical('Потеряно соединение с сервером.')
        exit(1)


@log
# Функция взаимодействия с пользователем, запрашивает команды, отправляет сообщения
def user_interactive(sock, username):
    print_help()
    while True:
        command = input('Введите команду: ')
        if command == 'message':
            create_message(sock, username)
        elif command == 'help':
            print_help()
        elif command == 'exit':
            send_message(sock, create_exit_message(username))
            print('Завершение соединения.')
            logger.info('Завершение работы по команде пользователя.')
            # Задержка неоходима, чтобы успело уйти сообщение о выходе
            time.sleep(0.5)
            break
        else:
            print('Команда не распознана, попробойте снова. help - вывести поддерживаемые команды.')


# Функция генерирует запрос о присутствии клиента
@log
def create_presence(account_name):
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    logger.debug(f'Сформировано {PRESENCE} сообщение для пользователя {account_name}')
    return out


# Функция выводящяя справку по использованию.
def print_help():
    print('Поддерживаемые команды:')
    print('message - отправить сообщение. Кому и текст будет запрошены отдельно.')
    print('help - вывести подсказки по командам')
    print('exit - выход из программы')


# Функция разбирает ответ сервера на сообщение о присутствии, возращает 200 если все ОК или генерирует исключение при\
# ошибке.
@log
def process_response_ans(message):
    logger.debug(f'Разбор приветственного сообщения от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        elif message[RESPONSE] == 400:
            raise ServerError(f'400 : {message[ERROR]}')
    raise ReqFieldMissingError(RESPONSE)


# Парсер аргументов коммандной строки
@log
def parse_client_argv():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-n', '--name', default=None, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_name = namespace.name

    # проверим подходящий номер порта
    if not 1023 < server_port < 65536:
        logger.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}. '
            f'Допустимы адреса с 1024 до 65535. Клиент завершается.')
        exit(1)

    return server_address, server_port, client_name


def main():
    # Сообщаем о запуске
    print('Консольный месседжер. Клиентский модуль.')

    # Загружаем параметы коммандной строки
    server_address, server_port, client_name = parse_client_argv()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_address, server_port))

    # Если имя пользователя не было задано, необходимо запросить пользователя.
    if not client_name:
        client_name = input('Введите имя пользователя>>> ')

    logger.info(
        f'Запущен клиент с парамертами: адрес сервера: {server_address}, порт: {server_port}, '
        f'имя пользователя: {client_name}')

    # Инициализация сокета и сообщение серверу о нашем появлении
    try:
        send_message(sock, create_presence(client_name))
        answer = process_response_ans(get_message(sock))

        logger.info(f'Установлено соединение с сервером. Ответ сервера: {answer}')
        print(f'Установлено соединение с сервером.')

    except json.JSONDecodeError:
        logger.error('Не удалось декодировать полученную Json строку.')
        exit(1)
    except ServerError as error:
        logger.error(f'При установке соединения сервер вернул ошибку: {error.text}')
        exit(1)
    except ReqFieldMissingError as missing_error:
        logger.error(f'В ответе сервера отсутствует необходимое поле {missing_error.missing_field}')
        exit(1)
    except (ConnectionRefusedError, ConnectionError):
        logger.critical(
            f'Не удалось подключиться к серверу {server_address}:{server_port}, '
            f'конечный компьютер отверг запрос на подключение.')
        exit(1)
    else:
        # Если соединение с сервером установлено корректно, запускаем клиенский процесс приёма сообщний
        receiver = threading.Thread(target=message_from_server, args=(sock, client_name))
        receiver.daemon = True
        receiver.start()

        # затем запускаем отправку сообщений и взаимодействие с пользователем.
        user_interface = threading.Thread(target=user_interactive, args=(sock, client_name))
        user_interface.daemon = True
        user_interface.start()

        logger.info(f'Клиент {client_name} online')

        # Watchdog основной цикл, если один из потоков завершён, то значит или потеряно соединение или пользователь
        # ввёл exit. Поскольку все события обработываются в потоках, достаточно просто завершить цикл.
        while True:
            time.sleep(1)
            if receiver.is_alive() and user_interface.is_alive():
                continue
            break


if __name__ == '__main__':
    main()
