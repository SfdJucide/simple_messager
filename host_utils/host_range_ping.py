import os
import ipaddress


def host_range_ping():
    addresses = [ipaddress.ip_address('127.0.16.1') + i for i in range(10)]
    for ip in addresses:
        response = os.system(f'ping -c 1 {ip}')

        if response == 0:
            print('Узел доступен!')
        else:
            print('Узел недоступен!')


if __name__ == '__main__':
    host_range_ping()
