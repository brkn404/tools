import dns.resolver
import time

def check_spf(domain, retries=3, delay=5):
    while retries > 0:
        try:
            resolver = dns.resolver.Resolver()
            resolver.nameservers = ['8.8.8.8', '8.8.4.4', '1.1.1.1', '9.9.9.9']  # Google's, Cloudflare's, and Quad9's DNS servers
            resolver.timeout = 10  # Increased timeout to 10 seconds
            resolver.lifetime = 10  # Increased lifetime to 10 seconds
            answers = resolver.resolve(domain, 'TXT')
            for rdata in answers:
                for txt_record in rdata.strings:
                    if txt_record.startswith(b'v=spf1'):
                        return txt_record.decode('utf-8')
        except dns.resolver.NoAnswer:
            return "No SPF record found."
        except dns.resolver.NXDOMAIN:
            return "Domain does not exist."
        except dns.exception.Timeout:
            retries -= 1
            if retries > 0:
                print("The DNS operation timed out. Retrying...")
                time.sleep(delay)
            else:
                return "The DNS operation timed out after multiple attempts."
        except Exception as e:
            return f"An error occurred: {e}"

def check_dmarc(domain, retries=3, delay=5):
    while retries > 0:
        try:
            dmarc_domain = f'_dmarc.{domain}'
            resolver = dns.resolver.Resolver()
            resolver.nameservers = ['8.8.8.8', '8.8.4.4', '1.1.1.1', '9.9.9.9']  # Google's, Cloudflare's, and Quad9's DNS servers
            resolver.timeout = 10  # Increased timeout to 10 seconds
            resolver.lifetime = 10  # Increased lifetime to 10 seconds
            answers = resolver.resolve(dmarc_domain, 'TXT')
            for rdata in answers:
                for txt_record in rdata.strings:
                    if txt_record.startswith(b'v=DMARC1'):
                        return txt_record.decode('utf-8')
        except dns.resolver.NoAnswer:
            return "No DMARC record found."
        except dns.resolver.NXDOMAIN:
            return "Domain does not exist."
        except dns.exception.Timeout:
            retries -= 1
            if retries > 0:
                print("The DNS operation timed out. Retrying...")
                time.sleep(delay)
            else:
                return "The DNS operation timed out after multiple attempts."
        except Exception as e:
            return f"An error occurred: {e}"

def main():
    domain = input("Enter the target domain: ")
    spf_record = check_spf(domain)
    dmarc_record = check_dmarc(domain)

    if spf_record:
        print(f"SPF record for {domain}: {spf_record}")
    else:
        print(f"No SPF record found for {domain}.")

    if dmarc_record:
        print(f"DMARC record for {domain}: {dmarc_record}")
    else:
        print(f"No DMARC record found for {domain}.")

if __name__ == "__main__":
    main()
