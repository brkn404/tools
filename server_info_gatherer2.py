import socket
import requests
import whois as whois_lib
from scapy.all import *
from dns import resolver
import json
from datetime import datetime
from requests.structures import CaseInsensitiveDict
import subprocess

def get_ip_info(ip):
    response = requests.get(f"https://ipinfo.io/{ip}/json")
    return response.json()

def get_whois_info(domain):
    return whois_lib.whois(domain)

def get_dns_info(domain):
    dns_info = {}
    try:
        dns_info['A'] = [str(rdata) for rdata in resolver.resolve(domain, 'A')]
        dns_info['AAAA'] = [str(rdata) for rdata in resolver.resolve(domain, 'AAAA')]
        dns_info['MX'] = [str(rdata.exchange) for rdata in resolver.resolve(domain, 'MX')]
        dns_info['NS'] = [str(rdata) for rdata in resolver.resolve(domain, 'NS')]
        dns_info['TXT'] = [str(rdata) for rdata in resolver.resolve(domain, 'TXT')]
    except Exception as e:
        dns_info['error'] = str(e)
    return dns_info

def get_http_headers(domain):
    try:
        response = requests.head(f"http://{domain}", allow_redirects=True)
        return response.headers
    except Exception as e:
        return {'error': str(e)}

def scan_ports(ip):
    open_ports = []
    for port in range(1, 1025):  # Scanning first 1024 ports
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((ip, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    return open_ports

def get_technologies(domain):
    try:
        result = subprocess.run(['wappalyzer', domain, '--quiet', '--json'], capture_output=True, text=True)
        return json.loads(result.stdout)
    except Exception as e:
        return {'error': str(e)}

def gather_server_info(domain):
    info = {}

    # Resolve domain to IP
    ip = socket.gethostbyname(domain)
    info['IP'] = ip

    # Get IP information
    info['IP_Info'] = get_ip_info(ip)

    # Get Whois information
    info['Whois_Info'] = get_whois_info(domain)

    # Get DNS information
    info['DNS_Info'] = get_dns_info(domain)

    # Get HTTP headers
    info['HTTP_Headers'] = get_http_headers(domain)

    # Scan for open ports
    info['Open_Ports'] = scan_ports(ip)

    # Get Technologies used
    info['Technologies'] = get_technologies(domain)

    return info

def convert_to_serializable(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, CaseInsensitiveDict):
        return dict(obj)
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

if __name__ == "__main__":
    domain = input("Enter the domain to gather information: ")
    info = gather_server_info(domain)
    
    # Pretty-print the gathered information
    print(json.dumps(info, indent=4, default=convert_to_serializable))
