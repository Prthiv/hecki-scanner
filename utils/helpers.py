import subprocess
import re
import logging
import socket

def validate_domain(domain: str) -> bool:
    """Validate domain format."""
    pattern = r'^[a-zA-Z0-9][a-zA-Z0-9\-]{0,61}[a-zA-Z0-9](?:\.[a-zA-Z]{2,})+$'
    return bool(re.match(pattern, domain))

def validate_ip(ip: str) -> bool:
    """Validate IP address format."""
    pattern = r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$'
    return bool(re.match(pattern, ip))

def validate_domain_or_ip(target: str) -> bool:
    """Validate domain or IP format."""
    return validate_domain(target) or validate_ip(target)

def run_whois(domain: str) -> str:
    """Run WHOIS lookup on a domain."""
    try:
        result = subprocess.run(['whois', domain], capture_output=True, text=True, timeout=30)
        logging.info(f"WHOIS for {domain}:\n{result.stdout}")
        return result.stdout
    except subprocess.TimeoutExpired:
        logging.error(f"WHOIS timeout for {domain}")
        return "WHOIS lookup timed out"
    except Exception as e:
        logging.error(f"WHOIS error for {domain}: {str(e)}")
        return f"Error running WHOIS: {str(e)}"

def run_nmap_scan(target: str) -> str:
    """Run basic Nmap scan on target (top 1000 ports)."""
    try:
        # Resolve domain to IP if necessary
        ip = socket.gethostbyname(target) if validate_domain(target) else target
        result = subprocess.run(['nmap', '-F', ip], capture_output=True, text=True, timeout=60)
        logging.info(f"Nmap scan for {target}:\n{result.stdout}")
        return result.stdout
    except subprocess.TimeoutExpired:
        logging.error(f"Nmap timeout for {target}")
        return "Nmap scan timed out"
    except Exception as e:
        logging.error(f"Nmap error for {target}: {str(e)}")
        return f"Error running Nmap: {str(e)}"

def run_sublist3r(domain: str) -> list:
    """Run Sublist3r and parse real subdomain results from output."""
    try:
        result = subprocess.run(
            ['sublist3r', '-d', domain],
            capture_output=True,
            text=True,
            timeout=120
        )

        output_lines = result.stdout.splitlines()

        # Filter only lines that look like subdomains
        subdomains = [
            line.strip()
            for line in output_lines
            if line.strip() and '.' in line and not line.startswith('[') and not line.startswith(' _')
        ]

        logging.info(f"Subdomains for {domain}: {subdomains}")
        return subdomains
    except subprocess.TimeoutExpired:
        logging.error(f"Sublist3r timeout for {domain}")
        return []
    except Exception as e:
        logging.error(f"Sublist3r error for {domain}: {str(e)}")
        return []



def resolve_ip_or_domain(target: str) -> str:
    """Resolve domain to IP or IP to hostname using socket."""
    try:
        if validate_domain(target):
            ip = socket.gethostbyname(target)
            logging.info(f"Resolved {target} to IP: {ip}")
            return f"Domain: {target}\nIP: {ip}"
        elif validate_ip(target):
            hostname = socket.gethostbyaddr(target)[0]
            logging.info(f"Resolved {target} to hostname: {hostname}")
            return f"IP: {target}\nHostname: {hostname}"
        else:
            raise ValueError("Invalid input")
    except socket.gaierror:
        logging.error(f"Resolution failed for {target}")
        return f"Could not resolve {target}"
    except Exception as e:
        logging.error(f"Resolution error for {target}: {str(e)}")
        return f"Error resolving {target}: {str(e)}"

def clear_log_file(log_path: str = 'logs/recon.log') -> bool:
    """Clear the contents of a log file.
    
    Args:
        log_path: Path to the log file to clear
        
    Returns:
        bool: True if successful, False if error occurred
    """
    try:
        with open(log_path, 'w') as f:
            f.write('')
        logging.info(f"Cleared log file at {log_path}")
        return True
    except FileNotFoundError:
        logging.error(f"Log file not found at {log_path}")
        return False
    except Exception as e:
        logging.error(f"Error clearing log file: {str(e)}")
        return False