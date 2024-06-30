import subprocess
import concurrent.futures
import socket
import csv
import sys
import json
import os
from datetime import datetime

def ping_host(ip, count, timeout):
    result = subprocess.run(['ping', '-c', str(count), '-W', str(timeout), ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        return ip
    return None

def port_scan(ip, ports):
    open_ports = []
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((ip, port))
            open_ports.append(port)
        except (socket.timeout, socket.error):
            pass
        finally:
            sock.close()
    return open_ports

def ping_sweep(network_prefix, count, timeout):
    active_hosts = []
    
    print(f"Starting ping sweep on network {network_prefix}.0/24...\n")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        future_to_ip = {executor.submit(ping_host, f"{network_prefix}.{host}", count, timeout): f"{network_prefix}.{host}" for host in range(1, 255)}
        
        for future in concurrent.futures.as_completed(future_to_ip):
            ip = future_to_ip[future]
            try:
                result = future.result()
                if result:
                    active_hosts.append(result)
                    print(f"\n{result} is active")
            except Exception as exc:
                print(f"\n{ip} generated an exception: {exc}")

    return sorted(active_hosts, key=lambda ip: int(ip.split('.')[-1]))

def save_results_to_csv(active_hosts, port_scan_results, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["IP Address", "Open Ports"])
        for ip in active_hosts:
            ports = ", ".join(map(str, port_scan_results.get(ip, [])))
            writer.writerow([ip, ports])

def save_results_to_json(active_hosts, port_scan_results, filename):
    results = {ip: port_scan_results.get(ip, []) for ip in active_hosts}
    with open(filename, 'w') as file:
        json.dump(results, file, indent=4)

if __name__ == "__main__":
    network_prefix = input("Enter the network prefix (e.g., 192.168.1): ")
    ping_count = int(input("Enter the number of ping attempts (default is 1): ") or 1)
    ping_timeout = int(input("Enter the ping timeout in seconds (default is 1): ") or 1)
    scan_ports = input("Enter the ports to scan (e.g., 20-25,80,443) or leave empty to skip port scan: ")
    
    if scan_ports:
        ports = []
        for part in scan_ports.split(','):
            if '-' in part:
                start, end = map(int, part.split('-'))
                ports.extend(range(start, end + 1))
            else:
                ports.append(int(part))
    else:
        ports = []

    active_hosts = ping_sweep(network_prefix, ping_count, ping_timeout)
    port_scan_results = {}

    if ports:
        print("\nStarting port scan...\n")
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            future_to_ip = {executor.submit(port_scan, ip, ports): ip for ip in active_hosts}
            
            for future in concurrent.futures.as_completed(future_to_ip):
                ip = future_to_ip[future]
                try:
                    open_ports = future.result()
                    if open_ports:
                        port_scan_results[ip] = open_ports
                        print(f"\n{ip} open ports: {', '.join(map(str, open_ports))}")
                except Exception as exc:
                    print(f"\n{ip} generated an exception: {exc}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"network_scan_results_{timestamp}.csv"
    json_filename = f"network_scan_results_{timestamp}.json"

    save_results_to_csv(active_hosts, port_scan_results, csv_filename)
    save_results_to_json(active_hosts, port_scan_results, json_filename)
    
    print("\n\nScan complete.\n")
    if active_hosts:
        print("Active hosts in the network:")
        for host in active_hosts:
            print(host)
    else:
        print("No active hosts found in the network.")
    
    print(f"\nResults saved to {csv_filename} and {json_filename}")
