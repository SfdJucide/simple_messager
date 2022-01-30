from subprocess import Popen, CREATE_NEW_CONSOLE
from threading import Thread
import random


def run_clients():
    addr, port, mode = ('127.0.0.5', '9999', ('listen', 'send'))
    with Popen(f'python client.py {addr} {port} {mode[random.randint(0, 1)]}',
               creationflags=CREATE_NEW_CONSOLE) as p:
        p.wait()


if __name__ == '__main__':
    number_of_clients = int(input('Введите кол-во запускаемых участников чата >> '))
    for i in range(number_of_clients):
        Thread(target=run_clients).start()
