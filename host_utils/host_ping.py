import os
import ipaddress


def host_ping(addresses):
    for ip in addresses:
        ip4 = ipaddress.ip_address(ip)
        response = os.system(f'ping -c 1 {ip4}')

        if response == 0:
            print('Узел доступен!')
        else:
            print('Узел недоступен!')


if __name__ == '__main__':
    host_ping(['127.0.0.1', '255.255.245.16', '255.214.34.3', '77.9.0.2'])
