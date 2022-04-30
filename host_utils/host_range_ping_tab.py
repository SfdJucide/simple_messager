import os
import ipaddress
from tabulate import tabulate


def host_range_ping_tab():
    dict_ip = {'reachable': [],
               'unreachable': []}
    addresses = [ipaddress.ip_address('77.99.0.124') + i for i in range(4)]
    for ip in addresses:
        response = os.system(f'ping -c 1 {ip}')

        if response == 0:
            dict_ip['reachable'].append(ip)
        else:
            dict_ip['unreachable'].append(ip)

    print(tabulate(dict_ip, headers='keys', tablefmt='pipe'))


if __name__ == '__main__':
    host_range_ping_tab()
