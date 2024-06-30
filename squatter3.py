import whois
import requests
import logging
import dns.resolver
import ssl
import socket
from pprint import pprint

logging.basicConfig(filename='squatting_detection.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def get_similar_domains(base_domain):
    base_name = base_domain.split('.')[0]
    tlds = ['com', 'net', 'org', 'co', 'info', 'biz', 'us', 'uk', 'ca', 'io']
    variations = [f"{base_name}.{tld}" for tld in tlds]
    return variations

def get_potential_subdomains(base_domain):
    subdomains = [
        'www', 'mail', 'admin', 'login', 'portal', 'secure', 'webmail', 'ftp', 'cpanel', 'blog', 'shop', 'support', 'dev', 'test', 'api', 'staging'
    ]
    potential_subdomains = [f"{sub}.{base_domain}" for sub in subdomains]
    return potential_subdomains

def check_domain_availability(domain):
    try:
        w = whois.whois(domain)
        return w.domain_name is None
    except Exception as e:
        logging.warning(f"WHOIS check failed for {domain}: {e}")
        return True

def check_domain_expiration(domain):
    try:
        w = whois.whois(domain)
        if w.expiration_date:
            if isinstance(w.expiration_date, list):
                expiration_date = w.expiration_date[0]
            else:
                expiration_date = w.expiration_date
            if expiration_date:
                return expiration_date
        return None
    except Exception as e:
        logging.warning(f"WHOIS check failed for {domain}: {e}")
        return None

def get_dns_record(subdomain):
    try:
        answers = dns.resolver.resolve(subdomain, 'CNAME')
        for rdata in answers:
            return 'CNAME', rdata.target.to_text()
    except dns.resolver.NoAnswer:
        try:
            answers = dns.resolver.resolve(subdomain, 'A')
            for rdata in answers:
                return 'A', rdata.to_text()
        except dns.resolver.NoAnswer:
            return None, None
    except dns.resolver.NXDOMAIN:
        return None, None

def check_ssl_certificate(domain):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                return cert
    except Exception as e:
        logging.warning(f"SSL certificate check failed for {domain}: {e}")
        return None

def check_http_status_and_content(domain):
    try:
        response = requests.get(f"http://{domain}", timeout=5)
        if response.status_code == 200:
            return response.status_code, response.headers, response.text[:500]
        else:
            return response.status_code, response.headers, None
    except requests.RequestException as e:
        logging.warning(f"HTTP request failed for {domain}: {e}")
        return None, None, None

def detect_squatting(base_domain):
    similar_domains = get_similar_domains(base_domain)
    squatting_domains = []
    for domain in similar_domains:
        if check_domain_availability(domain):
            squatting_domains.append(domain)
            logging.info(f"Potential squatting domain detected: {domain}")
    return squatting_domains

def detect_subdomain_squatting(base_domain):
    potential_subdomains = get_potential_subdomains(base_domain)
    squatting_subdomains = []
    for subdomain in potential_subdomains:
        status_code, headers, body_snippet = check_http_status_and_content(subdomain)
        if not status_code or status_code != 200:
            squatting_subdomains.append(subdomain)
            logging.info(f"Potential squatting subdomain detected: {subdomain}")
    return squatting_subdomains

def detect_domain_takeover(base_domain):
    expiration_date = check_domain_expiration(base_domain)
    if expiration_date:
        logging.info(f"Domain {base_domain} expires on {expiration_date}")
        print(f"Domain {base_domain} expires on {expiration_date}")

    potential_subdomains = get_potential_subdomains(base_domain)
    orphaned_subdomains = []
    for subdomain in potential_subdomains:
        dns_record_type, dns_record_target = get_dns_record(subdomain)
        status_code, headers, body_snippet = check_http_status_and_content(subdomain)
        ssl_cert = check_ssl_certificate(subdomain)

        details = {
            "DNS Record Type": dns_record_type,
            "DNS Record Target": dns_record_target,
            "HTTP Status": status_code,
            "HTTP Headers": headers,
            "HTTP Body Snippet": body_snippet,
            "SSL Certificate": ssl_cert
        }

        if not dns_record_type or not status_code or status_code != 200:
            orphaned_subdomains.append((subdomain, details))
            logging.info(f"Potential orphaned subdomain detected: {subdomain} with details: {details}")
            print(f"Potential orphaned subdomain detected: {subdomain}")
            pprint(details)

    return orphaned_subdomains

def main():
    import sys
    if len(sys.argv) != 2:
        print("Usage: python squatter.py <domain>")
        sys.exit(1)
        
    base_domain = sys.argv[1]
    squatting_domains = detect_squatting(base_domain)
    print("Potential Squatting Domains:")
    pprint(squatting_domains)
    
    squatting_subdomains = detect_subdomain_squatting(base_domain)
    print("Potential Squatting Subdomains:")
    pprint(squatting_subdomains)
    
    orphaned_subdomains = detect_domain_takeover(base_domain)
    print("Potential Orphaned Subdomains:")
    pprint(orphaned_subdomains)

    for domain in squatting_domains:
        check_http_status_and_content(domain)
        cert = check_ssl_certificate(domain)
        if cert:
            logging.info(f"Domain {domain} has a valid SSL certificate: {cert}")
            print(f"Domain {domain} has a valid SSL certificate:")
            pprint(cert)

if __name__ == "__main__":
    main()
