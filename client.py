from sys import argv
import json
import time
from socket import socket, AF_INET, SOCK_STREAM


def build_message(user):
    presence_message = {
        'action': 'presence',
        'time': time.time(),
        'user': user
    }
    return presence_message


def parse_client_argv(args):
    try:
        addr = args[1]
        port = int(args[2])
    except IndexError:
        addr = 'localhost'
        port = 7777

    return addr, port


def check_server_answer(response):
    if response['response'] == 200:
        h_response = '200: OK'
    else:
        h_response = '400: Bad Request'
    return h_response


def run_client():
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(parse_client_argv(argv))
    message = build_message('guest')
    json_message = json.dumps(message)
    s.send(json_message.encode('utf-8'))

    data = s.recv(100000)
    json_data = data.decode('utf-8')
    response = json.loads(json_data)

    h_response = check_server_answer(response)

    print(f'Server answer: {response}')
    print(h_response)


if __name__ == '__main__':
    run_client()
