'''
Check HTTP connectivity with in a traceroute way from the client
computer to the internet.
'''
import getpass
from socket import AF_INET
from pyroute2 import IPRoute
import requests

AP = IPRoute().get_default_routes(family=AF_INET)[0].get_attr('RTA_GATEWAY')

HOSTS = [
    {'name': 'AP', 'ip': AP},
    {'name': 'CPE', 'ip': '192.168.1.1'},
    {'name': 'AYTO', 'ip': '10.34.192.97'},
    {'name': 'EMITA', 'ip': '10.34.192.113'},
    {'name': 'PROXY', 'ip': '10.34.192.66'}
]

def is_alive(addr, proxies=None):
    '''
    Perform an HTTP request to the desired host.
    '''
    try:
        resp = requests.get('http://%s/' % addr, proxies=proxies, timeout=1)
    except requests.exceptions.Timeout:
        return 'Timeout'
    if resp.status_code == 200:
        return 'OK!'
    return ':('

if __name__ == "__main__":
    for host in HOSTS:
        name = host.get('name')
        ip = host.get('ip')
        print('%-12s %-16s %-10s' % (name, ip, is_alive(ip)))
        if 'PROXY' in name:
            proxyAddr = ip

    USER = input(' Introduce tu nombre de usuario para el proxy: ')
    PASSWORD = getpass.getpass(' Introduce tu contraseña para el proxy: ')
    PROXY = {'http': 'http://%s:%s@%s:3128/' % (USER, PASSWORD, proxyAddr)}
    print('%-12s %-16s %-10s' % ('GOOGLE', '8.8.8.8', is_alive('8.8.8.8', PROXY)))
