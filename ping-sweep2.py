import subprocess
import concurrent.futures
import sys

def ping_host(ip):
    result = subprocess.run(['ping', '-c', '1', '-W', '1', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        return ip
    return None

def ping_sweep(network_prefix):
    active_hosts = []
    
    print(f"Starting ping sweep on network {network_prefix}.0/24...\n")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        future_to_ip = {executor.submit(ping_host, f"{network_prefix}.{host}"): f"{network_prefix}.{host}" for host in range(1, 255)}
        
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

if __name__ == "__main__":
    network_prefix = input("Enter the network prefix (e.g., 192.168.1): ")
    active_hosts = ping_sweep(network_prefix)
    
    print("\n\nPing sweep complete.\n")
    if active_hosts:
        print("Active hosts in the network:")
        for host in active_hosts:
            print(host)
    else:
        print("No active hosts found in the network.")
