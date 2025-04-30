import base64
import os
import sys
import platform
import getpass
import hashlib
import socket
import string
import secrets
import binascii
import ipaddress 
from datetime import datetime


try:
    from cryptography.fernet import Fernet, InvalidToken
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
except ImportError:
    print("ERROR: 'cryptography' library not found. Please run installer script or install manually (pip install cryptography)")
    sys.exit(1)

try:
    import requests
    from requests.exceptions import RequestException
except ImportError:
    print("ERROR: 'requests' library not found. Please run installer script or install manually (pip install requests)")
    sys.exit(1)

try:
    import whois
except ImportError:
    print("ERROR: 'python-whois' library not found. Please run installer script or install manually (pip install python-whois)")
    sys.exit(1)

try:
    import dns.resolver
    import dns.exception
except ImportError:
    print("ERROR: 'dnspython' library not found. Please run installer script or install manually (pip install dnspython)")
    sys.exit(1)

try:
    import psutil
except ImportError:
    print("ERROR: 'psutil' library not found. Please run installer script or install manually (pip install psutil)")
    sys.exit(1)



GREEN = '\033[0;32m'
RED = '\033[0;31m'
CYAN = '\033[0;36m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
MAGENTA = '\033[0;35m'
WHITE = '\033[1;37m'
NC = '\033[0m' 


ASCII_ART = f"""{CYAN}
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣤⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣾⠿⠛⠋⠉⠉⠙⠛⠿⣷⣤⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣠⣾⠟⢁⣤⣾⠿⠟⠻⠿⣷⣤⡈⠻⣿⣄⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣿⡏⢀⣾⡿⠁⠀⠀⠀⠀⠈⢿⣿⡀⢹⣿⡀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢸⣿⠀⣼⣿⠀⠀⠀⠀⠀⠀⠀⠀⢿⣷⠀⣿⡇⠀⠀⠀
⠀⠀⠀⠀⠀⣠⣼⣿⣤⣿⣿⣤⣤⣤⣤⣤⣤⣤⣤⣼⣿⣤⣿⣧⣄⠀⠀
⠀⠀⠀⢠⣿⠟⣉⣩⣉⣉⣉⣉⣩⣉⣉⣉⣉⣉⣉⣩⣉⣉⣉⣍⠻⣿⡄
⠀⠀⠀⣞⠉⠈⠉⠉⢙⣿⣿⣿⠿⠛⠛⠛⠛⠿⣿⣿⣿⡋⠉⠉⠁⠉⣳
⠀⠀⠀⣸⠿⠿⠿⣿⣿⣿⠏⢀⣴⡶⠿⠿⢶⣦⡀⠹⣿⣿⣿⠿⠿⠿⢇
⠀⠀⠀⢱⣶⣶⣶⣿⣿⡏⢠⣿⠏⢠⣶⣶⡄⠙⣿⡄⢹⣿⣿⣶⣶⣶⡏
⠀⠀⠀⢻⣤⣤⣤⣿⣿⡄⢸⣿⠀⢘⣿⣿⡃⠀⣿⡇⢀⣿⣿⣤⣤⣤⡝
⠀⠀⠀⣞⠉⠉⠙⣿⣿⣷⠀⠻⠇⢸⡇⢸⡇⢸⠟⠀⣼⣿⣿⠋⠉⠉⣷
⠀⠀⠀⢸⣿⢿⡿⣿⢿⣿⣿⡀⠀⠸⢿⡿⠏⠀⢀⣾⣿⣿⡿⣿⡿⣿⡇
⠀⠀⠀⢻⣤⠤⣤⣤⣤⣿⣿⣿⣷⣦⣤⣤⣴⣾⣿⣿⣿⣤⣤⣤⠤⣤⡞
⠀⠀⠀⠈⢿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⡿⠁
⠀⠀⠀⠀⠀⠉⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠉⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀
      EVIL LOCK MULTI-TOOL
{NC}"""


AUTHOR_INFO = f"""{GREEN}=============================================================={NC}
{YELLOW} Tool Version : {WHITE}6.6.6{NC}
{YELLOW} Author       : {CYAN}Pyscodes-pro{NC}
{YELLOW} Instagram    : {CYAN}https://instagram.com/pyscodes{NC}
{YELLOW} GitHub       : {CYAN}https://github.com/Pyscodes-pro{NC}
{GREEN}=============================================================={NC}"""


def clear_screen():
    command = 'cls' if platform.system().lower() == 'windows' else 'clear'
    os.system(command)

def display_header():
    print(ASCII_ART)
    print(AUTHOR_INFO)
    print()

def pause_and_continue(message=f"\n{YELLOW}Press Enter to continue...{NC}"):
    input(message)

def get_password(prompt=f"{CYAN}Enter secret key (input hidden): {NC}"):
    try:
        p = getpass.getpass(prompt)
        if not p:
            print(f"{RED}[!] Secret key cannot be empty.{NC}")
            return None
        return p
    except Exception as e:
        print(f"{RED}[!] Error reading secret key: {e}{NC}")
        return None
    except KeyboardInterrupt:
        print(f"\n{RED}[!] Operation cancelled by user.{NC}")
        return None

def is_valid_ip(address):
    try:
        ipaddress.ip_address(address)
        return True
    except ValueError:
        return False


def generate_salt():
    return os.urandom(16)

def derive_key(password: bytes, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key

def encrypt_message(password: str, message: str):
    try:
        salt = generate_salt()
        key = derive_key(password.encode(), salt)
        f = Fernet(key)
        encrypted_message = f.encrypt(message.encode())
        return base64.urlsafe_b64encode(salt + encrypted_message).decode()
    except Exception as e:
        print(f"{RED}[!] Encryption Error (Message): {e}{NC}")
        return None

def decrypt_message(password: str, encrypted_data_b64: str):
    try:
        encrypted_data = base64.urlsafe_b64decode(encrypted_data_b64.encode())
        salt = encrypted_data[:16]
        token = encrypted_data[16:]
        key = derive_key(password.encode(), salt)
        f = Fernet(key)
        decrypted_message = f.decrypt(token).decode()
        return decrypted_message
    except InvalidToken:
        print(f"{RED}[!] Decryption Error (Message): Invalid key or corrupted data.{NC}")
        return None
    except Exception as e:
        print(f"{RED}[!] Decryption Error (Message): {e}{NC}")
        return None

def encrypt_file(password: str, input_filepath: str, output_filepath: str):
    try:
        salt = generate_salt()
        key = derive_key(password.encode(), salt)
        f = Fernet(key)
        with open(input_filepath, 'rb') as file:
            file_data = file.read()
        encrypted_data = f.encrypt(file_data)
        with open(output_filepath, 'wb') as file:
            file.write(salt)
            file.write(encrypted_data)
        return True
    except FileNotFoundError:
        print(f"{RED}[!] Encryption Error (File): Input file not found: '{input_filepath}'{NC}")
        return False
    except PermissionError:
         print(f"{RED}[!] Encryption Error (File): Permission denied for '{input_filepath}' or '{output_filepath}'.{NC}")
         return False
    except Exception as e:
        print(f"{RED}[!] Encryption Error (File): {e}{NC}")
        return False

def decrypt_file(password: str, input_filepath: str, output_filepath: str):
    try:
        with open(input_filepath, 'rb') as file:
            salt = file.read(16)
            encrypted_data = file.read()
        key = derive_key(password.encode(), salt)
        f = Fernet(key)
        decrypted_data = f.decrypt(encrypted_data)
        with open(output_filepath, 'wb') as file:
            file.write(decrypted_data)
        return True
    except FileNotFoundError:
        print(f"{RED}[!] Decryption Error (File): Input file not found: '{input_filepath}'{NC}")
        return False
    except InvalidToken:
         print(f"{RED}[!] Decryption Error (File): Invalid key or corrupted data in '{input_filepath}'.{NC}")
         return False
    except PermissionError:
         print(f"{RED}[!] Decryption Error (File): Permission denied for '{input_filepath}' or '{output_filepath}'.{NC}")
         return False
    except Exception as e:
        print(f"{RED}[!] Decryption Error (File): {e}{NC}")
        return False

def calculate_hash():
    print(f"{MAGENTA}--- Hash Calculator ---{NC}")
    print(f"{YELLOW}[1] Hash Text Input")
    print(f"{YELLOW}[2] Hash File")
    print(f"{YELLOW}[0] Back to Crypto Menu{NC}")
    choice = input(f"{CYAN}Select hash source: {NC}")

    if choice not in ['1', '2']:
        if choice != '0': print(f"{RED}Invalid choice.{NC}")
        return

    hash_algos = {'1': hashlib.md5, '2': hashlib.sha1, '3': hashlib.sha256, '4': hashlib.sha512}
    print(f"\n{YELLOW}Available Algorithms:{NC}")
    print(f"{YELLOW}[1] MD5")
    print(f"{YELLOW}[2] SHA-1")
    print(f"{YELLOW}[3] SHA-256")
    print(f"{YELLOW}[4] SHA-512")
    algo_choice = input(f"{CYAN}Select algorithm: {NC}")

    if algo_choice not in hash_algos:
        print(f"{RED}Invalid algorithm choice.{NC}")
        return

    hasher = hash_algos[algo_choice]()
    algo_name = ['MD5', 'SHA-1', 'SHA-256', 'SHA-512'][int(algo_choice)-1]

    try:
        if choice == '1':
            text_input = input(f"{CYAN}Enter text to hash: {NC}")
            if not text_input:
                print(f"{RED}Input text cannot be empty.{NC}")
                return
            hasher.update(text_input.encode())
            print(f"\n{GREEN}{algo_name} Hash:{NC} {WHITE}{hasher.hexdigest()}{NC}")

        elif choice == '2':
            file_path = input(f"{CYAN}Enter path to file: {NC}")
            if not os.path.isfile(file_path):
                print(f"{RED}File not found: '{file_path}'{NC}")
                return
            print(f"{YELLOW}Hashing file '{os.path.basename(file_path)}'...{NC}")
            with open(file_path, 'rb') as f:
                while True:
                    chunk = f.read(4096) 
                    if not chunk:
                        break
                    hasher.update(chunk)
            print(f"\n{GREEN}{algo_name} Hash:{NC} {WHITE}{hasher.hexdigest()}{NC}")

    except PermissionError:
         print(f"{RED}[!] Permission denied reading file.{NC}")
    except Exception as e:
        print(f"{RED}[!] Error during hashing: {e}{NC}")

def generate_password_tool():
     print(f"{MAGENTA}--- Strong Password Generator ---{NC}")
     try:
         length = int(input(f"{CYAN}Enter desired password length (e.g., 16): {NC}"))
         if length < 8:
             print(f"{YELLOW}Warning: Length less than 8 is generally not recommended.{NC}")
         if length <= 0:
              print(f"{RED}Length must be positive.{NC}")
              return

         use_uppercase = input(f"{CYAN}Include uppercase letters? (y/n): {NC}").lower() == 'y'
         use_lowercase = input(f"{CYAN}Include lowercase letters? (y/n): {NC}").lower() == 'y'
         use_digits = input(f"{CYAN}Include digits? (y/n): {NC}").lower() == 'y'
         use_symbols = input(f"{CYAN}Include symbols? (y/n): {NC}").lower() == 'y'

         character_set = ""
         if use_uppercase: character_set += string.ascii_uppercase
         if use_lowercase: character_set += string.ascii_lowercase
         if use_digits: character_set += string.digits
         if use_symbols: character_set += string.punctuation

         if not character_set:
             print(f"{RED}You must select at least one character set!{NC}")
             return

         password = ''.join(secrets.choice(character_set) for _ in range(length))
         print(f"\n{GREEN}Generated Password:{NC} {WHITE}{password}{NC}")

     except ValueError:
         print(f"{RED}Invalid length. Please enter a number.{NC}")
     except Exception as e:
         print(f"{RED}Error generating password: {e}{NC}")



def perform_port_scan():
    print(f"{MAGENTA}--- Basic Port Scanner ---{NC}")
    print(f"{RED}WARNING: Unauthorized scanning is illegal and unethical.{NC}")
    print(f"{YELLOW}Only scan targets you have explicit permission to test.{NC}")
    target = input(f"{CYAN}Enter target IP Address or Hostname: {NC}")
    if not target:
        print(f"{RED}Target cannot be empty.{NC}")
        return

    try:
        target_ip = socket.gethostbyname(target)
        print(f"{YELLOW}Resolved '{target}' to IP: {target_ip}{NC}")
    except socket.gaierror:
        print(f"{RED}Could not resolve hostname '{target}'. Check the name or your network connection.{NC}")
        return
    except Exception as e:
        print(f"{RED}Error resolving hostname: {e}{NC}")
        return

    port_range_str = input(f"{CYAN}Enter port range (e.g., 1-1024) or common ports (c): {NC}")
    ports_to_scan = []

    if port_range_str.lower() == 'c':
        ports_to_scan = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080]
        print(f"{YELLOW}Scanning common ports...{NC}")
    else:
        try:
            start_port, end_port = map(int, port_range_str.split('-'))
            if not (0 < start_port <= 65535 and 0 < end_port <= 65535 and start_port <= end_port):
                raise ValueError("Invalid port range.")
            ports_to_scan = range(start_port, end_port + 1)
            print(f"{YELLOW}Scanning ports {start_port}-{end_port}...{NC}")
        except ValueError:
            print(f"{RED}Invalid port range format. Use start-end (e.g., 80-100).{NC}")
            return

    open_ports = []
    socket.setdefaulttimeout(0.5) 
    print(f"{YELLOW}Starting scan on {target_ip}... (This may take a while){NC}")
    start_time = datetime.now()

    for port in ports_to_scan:

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((target_ip, port))
            if result == 0:
                print(f"{GREEN}[+] Port {port}: Open{NC}")
                open_ports.append(port)
            sock.close()
        except socket.error as e:
            
            pass
        except KeyboardInterrupt:
            print(f"\n{RED}Scan aborted by user.{NC}")
            return

    end_time = datetime.now()
    total_time = end_time - start_time
    print(f"\n{GREEN}Scan Complete.{NC}")
    if open_ports:
        print(f"{GREEN}Open ports found: {', '.join(map(str, sorted(open_ports)))}{NC}")
    else:
        print(f"{YELLOW}No open ports found in the specified range.{NC}")
    print(f"{YELLOW}Scan Duration: {total_time}{NC}")


def perform_whois_lookup():
    print(f"{MAGENTA}--- Whois Domain Lookup ---{NC}")
    domain = input(f"{CYAN}Enter domain name (e.g., google.com): {NC}")
    if not domain:
        print(f"{RED}Domain name cannot be empty.{NC}")
        return

    print(f"{YELLOW}Querying WHOIS for '{domain}'...{NC}")
    try:
        w = whois.whois(domain)
        if w.status is None and not w.domain_name : 
             print(f"{RED}Could not retrieve WHOIS data. Domain might not exist or WHOIS server unavailable.{NC}")
             if hasattr(w,'text'): 
                  print(f"{YELLOW}Raw Response Snippet:{NC}\n{w.text[:500]}...") 
        else:
             print(f"{GREEN}--- WHOIS Information ---{NC}")
            
             for key, value in w.items():
                 
                 if key != 'text' and value:
                     
                     if isinstance(value, list):
                         print(f"{YELLOW}{key.replace('_',' ').title():<20}:{NC} {', '.join(map(str, value))}")
                     else:
                         print(f"{YELLOW}{key.replace('_',' ').title():<20}:{NC} {value}")
             print(f"{GREEN}-------------------------{NC}")

    except whois.parser.PywhoisError as e:
        print(f"{RED}WHOIS Error: {e}{NC}")
    except Exception as e:
        print(f"{RED}An unexpected error occurred during WHOIS lookup: {e}{NC}")

def perform_dns_lookup():
    print(f"{MAGENTA}--- DNS Record Lookup ---{NC}")
    domain = input(f"{CYAN}Enter domain name (e.g., google.com): {NC}")
    if not domain:
        print(f"{RED}Domain name cannot be empty.{NC}")
        return

    record_types = ['A', 'AAAA', 'MX', 'TXT', 'NS', 'CNAME']
    print(f"{YELLOW}Querying DNS records for '{domain}'...{NC}")

    for rtype in record_types:
        try:
            print(f"{CYAN}Querying {rtype} records...{NC}")
            answers = dns.resolver.resolve(domain, rtype)
            print(f"{GREEN}--- {rtype} Records ---{NC}")
            for rdata in answers:
                print(f"  {GREEN}{rdata.to_text()}{NC}")

        except dns.resolver.NoAnswer:
            print(f"{YELLOW}  No {rtype} records found.{NC}")
        except dns.resolver.NXDOMAIN:
            print(f"{RED}Domain '{domain}' does not exist (NXDOMAIN).{NC}")
            return 
        except dns.exception.Timeout:
            print(f"{RED}DNS query timed out for {rtype} records.{NC}")
        except dns.resolver.NoNameservers:
             print(f"{RED}Could not contact nameservers for {rtype} records.{NC}")
        except Exception as e:
            print(f"{RED}Error querying {rtype} records: {e}{NC}")
        print("-" * 20)


def get_http_headers():
    print(f"{MAGENTA}--- HTTP Header Viewer ---{NC}")
    url = input(f"{CYAN}Enter full URL (e.g., https://google.com): {NC}")
    if not url:
        print(f"{RED}URL cannot be empty.{NC}")
        return

    if not url.startswith(('http://', 'https://')):
        print(f"{YELLOW}[!] URL scheme missing, attempting with 'https://'{NC}")
        url = 'https://' + url

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    print(f"{YELLOW}Fetching headers from '{url}'...{NC}")

    try:
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        
        print(f"{GREEN}--- Response Headers from {response.url} (Status: {response.status_code}) ---{NC}")
        if response.headers:
            for key, value in response.headers.items():
                print(f"{YELLOW}{key:<25}:{NC} {value}")
        else:
             print(f"{YELLOW}No headers received in the response.{NC}")
        print(f"{GREEN}------------------------------------------------------{NC}")

    except RequestException as e:
        print(f"{RED}[!] Network Error: Could not retrieve headers.{NC}")
        print(f"{RED}   Reason: {e}{NC}")
    except Exception as e:
        print(f"{RED}[!] An unexpected error occurred: {e}{NC}")


def get_website_cookies_feature(): 
    print(f"{MAGENTA}--- Website Cookie Viewer ---{NC}")
    url = input(f"{CYAN}Enter full URL (e.g., https://google.com): {NC}")
    if not url:
        print(f"{RED}URL cannot be empty.{NC}")
        return

    if not url.startswith(('http://', 'https://')):
        print(f"{YELLOW}[!] URL scheme missing, attempting with 'https://'{NC}")
        url = 'https://' + url

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    print(f"{YELLOW}Attempting connection to '{url}' to check cookies...{NC}")

    try:
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        response.raise_for_status() 
        if response.cookies:
            print(f"{GREEN}[+] Cookies received from {response.url} (Status: {response.status_code}):{NC}")
            for cookie in response.cookies:
                expires_str = "Session"
                if cookie.expires:
                     try:
                         expires_str = datetime.fromtimestamp(cookie.expires).strftime('%Y-%m-%d %H:%M:%S UTC')
                     except:
                         expires_str = str(cookie.expires)

                print(f"  - Name : {GREEN}{cookie.name}{NC}")
                print(f"    Value: {CYAN}{cookie.value}{NC}")
                print(f"    Domain: {cookie.domain}")
                print(f"    Path  : {cookie.path}")
                print(f"    Secure: {cookie.secure}")
                print(f"    Expires: {expires_str}")
                print("-" * 20)
        else:
            print(f"{YELLOW}[-] No cookies were set by the server in this response.{NC}")

    except RequestException as e:
        print(f"{RED}[!] Network Error: Could not retrieve data/cookies.{NC}")
        print(f"{RED}   Reason: {e}{NC}")
    except Exception as e:
        print(f"{RED}[!] An unexpected error occurred: {e}{NC}")



def encode_decode_data():
    print(f"{MAGENTA}--- Data Encoder/Decoder ---{NC}")
    print(f"{YELLOW}[1] Base64 Encode")
    print(f"{YELLOW}[2] Base64 Decode")
    print(f"{YELLOW}[3] Hex Encode")
    print(f"{YELLOW}[4] Hex Decode")
    print(f"{YELLOW}[0] Back to Data Utilities Menu{NC}")
    choice = input(f"{CYAN}Select operation: {NC}")

    if choice == '0': return
    if choice not in ['1', '2', '3', '4']:
        print(f"{RED}Invalid choice.{NC}")
        return

    data_input = input(f"{CYAN}Enter data: {NC}")
    if not data_input:
        print(f"{RED}Input data cannot be empty.{NC}")
        return

    try:
        result = None
        if choice == '1': 
            result = base64.b64encode(data_input.encode()).decode()
            print(f"\n{GREEN}Base64 Encoded:{NC} {WHITE}{result}{NC}")
        elif choice == '2':
            result = base64.b64decode(data_input.encode()).decode()
            print(f"\n{GREEN}Base64 Decoded:{NC} {WHITE}{result}{NC}")
        elif choice == '3': 
            result = binascii.hexlify(data_input.encode()).decode()
            print(f"\n{GREEN}Hex Encoded:{NC} {WHITE}{result}{NC}")
        elif choice == '4': 
            result = binascii.unhexlify(data_input.encode()).decode()
            print(f"\n{GREEN}Hex Decoded:{NC} {WHITE}{result}{NC}")

    except (binascii.Error, base64.binascii.Error, ValueError) as e:
         print(f"{RED}[!] Decoding Error: Invalid input data for the selected format. {e}{NC}")
    except UnicodeDecodeError:
         print(f"{RED}[!] Decoding Error: Result is not valid text (binary data?).{NC}")
         
    except Exception as e:
        print(f"{RED}[!] An unexpected error occurred: {e}{NC}")



def display_system_info():
    print(f"{MAGENTA}--- System Information ---{NC}")
    try:
        print(f"{YELLOW}{'OS Type':<20}:{NC} {platform.system()}")
        print(f"{YELLOW}{'OS Release':<20}:{NC} {platform.release()}")
        print(f"{YELLOW}{'OS Version':<20}:{NC} {platform.version()}")
        print(f"{YELLOW}{'Architecture':<20}:{NC} {platform.machine()}")
        print(f"{YELLOW}{'Processor':<20}:{NC} {platform.processor()}")
        print(f"{YELLOW}{'Hostname':<20}:{NC} {socket.gethostname()}")
        try:
            
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            print(f"{YELLOW}{'Local IP (Guess)':<20}:{NC} {local_ip}")
        except socket.gaierror:
             print(f"{YELLOW}{'Local IP (Guess)':<20}:{NC} {RED}Could not resolve hostname to IP{NC}")

        print(f"{YELLOW}{'Python Version':<20}:{NC} {sys.version.split()[0]}") 

        
        print(f"{GREEN}--- Resource Info (psutil) ---{NC}")
        cpu_count = psutil.cpu_count(logical=True)
        print(f"{YELLOW}{'CPU Cores (Logical)':<20}:{NC} {cpu_count}")
        mem = psutil.virtual_memory()
        mem_total_gb = mem.total / (1024**3)
        print(f"{YELLOW}{'Total RAM':<20}:{NC} {mem_total_gb:.2f} GB")

    except Exception as e:
        print(f"{RED}Error retrieving system info: {e}{NC}")

def list_running_processes():
    print(f"{MAGENTA}--- Running Processes ---{NC}")
    print(f"{YELLOW}{'PID':<8} {'Username':<15} {'Name'}{NC}")
    print("-" * 40)
    count = 0
    try:
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            try:
                pid = proc.info['pid']
                name = proc.info['name'] or 'N/A'
                username = proc.info['username'] or 'N/A'
                
                print(f"{WHITE}{pid:<8}{NC} {CYAN}{username[:15]:<15}{NC} {name[:40]}{NC}") 
                count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                
                pass
            except Exception as inner_e:
                 print(f"{RED}Error processing PID {proc.pid}: {inner_e}{NC}")
        print("-" * 40)
        print(f"{GREEN}Total processes listed: {count}{NC}")

    except Exception as e:
        print(f"{RED}Error retrieving process list: {e}{NC}")


# --- Menu Handlers ---
def handle_crypto_menu():
    while True:
        clear_screen()
        display_header()
        print(f"{BLUE}------- Cryptography Tools -------{NC}")
        print(f"{YELLOW}[1] Encrypt Text Message")
        print(f"{YELLOW}[2] Decrypt Text Message")
        print(f"{YELLOW}[3] Encrypt File")
        print(f"{YELLOW}[4] Decrypt File")
        print(f"{YELLOW}[5] Hash Calculator (MD5, SHA...)")
        print(f"{YELLOW}[6] Generate Strong Password")
        print(f"{MAGENTA}[0] Back to Main Menu{NC}")
        print(f"{BLUE}----------------------------------{NC}")
        choice = input(f"{YELLOW}>>> Select Crypto option [0-6]: {NC}")

        if choice == '1':
            password = get_password()
            if not password: pause_and_continue(); continue
            message = input(f"{CYAN}Enter the message to encrypt: {NC}")
            if not message: print(f"{RED}Message cannot be empty.{NC}"); pause_and_continue(); continue
            print(f"\n{YELLOW}[*] Encrypting...{NC}"); encrypted = encrypt_message(password, message)
            if encrypted: print(f"{GREEN}[+] Ciphertext:{NC} {WHITE}{encrypted}{NC}")
            pause_and_continue()
        elif choice == '2':
            password = get_password()
            if not password: pause_and_continue(); continue
            encrypted_data = input(f"{CYAN}Enter ciphertext: {NC}")
            if not encrypted_data: print(f"{RED}Ciphertext cannot be empty.{NC}"); pause_and_continue(); continue
            print(f"\n{YELLOW}[*] Decrypting...{NC}"); decrypted = decrypt_message(password, encrypted_data)
            if decrypted: print(f"{GREEN}[+] Plaintext:{NC} {WHITE}{decrypted}{NC}")
            pause_and_continue()
        elif choice == '3':
            password = get_password();
            if not password: pause_and_continue(); continue
            input_file = input(f"{CYAN}File to encrypt: {NC}")
            default_output = f"{input_file}.enc"; output_file = input(f"{CYAN}Output file (default: {default_output}): {NC}") or default_output
            if not os.path.exists(input_file): print(f"{RED}Input file not found.{NC}"); pause_and_continue(); continue
            if os.path.abspath(input_file) == os.path.abspath(output_file): print(f"{RED}Input/output cannot be same.{NC}"); pause_and_continue(); continue
            print(f"\n{YELLOW}[*] Encrypting file...{NC}"); success = encrypt_file(password, input_file, output_file)
            if success: print(f"{GREEN}[+] File encrypted successfully to '{output_file}'{NC}")
            pause_and_continue()
        elif choice == '4':
            password = get_password();
            if not password: pause_and_continue(); continue
            input_file = input(f"{CYAN}File to decrypt (.enc): {NC}")
            default_output = input_file.replace('.enc', '.dec') if input_file.endswith('.enc') else f"{input_file}.dec"
            output_file = input(f"{CYAN}Output file (default: {default_output}): {NC}") or default_output
            if not os.path.exists(input_file): print(f"{RED}Input file not found.{NC}"); pause_and_continue(); continue
            if os.path.abspath(input_file) == os.path.abspath(output_file): print(f"{RED}Input/output cannot be same.{NC}"); pause_and_continue(); continue
            print(f"\n{YELLOW}[*] Decrypting file...{NC}"); success = decrypt_file(password, input_file, output_file)
            if success: print(f"{GREEN}[+] File decrypted successfully to '{output_file}'{NC}")
            pause_and_continue()
        elif choice == '5':
             calculate_hash()
             pause_and_continue()
        elif choice == '6':
             generate_password_tool()
             pause_and_continue()
        elif choice == '0':
            break
        else:
            print(f"{RED}Invalid choice.{NC}")
            pause_and_continue()


def handle_network_menu():
     while True:
        clear_screen()
        display_header()
        print(f"{BLUE}--------- Network Tools ---------{NC}")
        print(f"{YELLOW}[1] Basic Port Scanner")
        print(f"{YELLOW}[2] Whois Domain Lookup")
        print(f"{YELLOW}[3] DNS Record Lookup")
        print(f"{YELLOW}[4] Get HTTP Headers")
        print(f"{YELLOW}[5] Get Website Cookies")
        print(f"{MAGENTA}[0] Back to Main Menu{NC}")
        print(f"{BLUE}---------------------------------{NC}")
        choice = input(f"{YELLOW}>>> Select Network option [0-5]: {NC}")

        if choice == '1':
            perform_port_scan()
            pause_and_continue()
        elif choice == '2':
            perform_whois_lookup()
            pause_and_continue()
        elif choice == '3':
            perform_dns_lookup()
            pause_and_continue()
        elif choice == '4':
            get_http_headers()
            pause_and_continue()
        elif choice == '5':
            get_website_cookies_feature()
            pause_and_continue()
        elif choice == '0':
            break
        else:
            print(f"{RED}Invalid choice.{NC}")
            pause_and_continue()


def handle_data_menu():
     while True:
        clear_screen()
        display_header()
        print(f"{BLUE}------- Data Utilities -------{NC}")
        print(f"{YELLOW}[1] Encode/Decode (Base64, Hex)")
        
        print(f"{MAGENTA}[0] Back to Main Menu{NC}")
        print(f"{BLUE}------------------------------{NC}")
        choice = input(f"{YELLOW}>>> Select Data option [0-1]: {NC}") 

        if choice == '1':
            encode_decode_data()
            pause_and_continue()
        elif choice == '0':
            break
        else:
            print(f"{RED}Invalid choice.{NC}")
            pause_and_continue()


def handle_system_menu():
      while True:
        clear_screen()
        display_header()
        print(f"{BLUE}------- System Utilities -------{NC}")
        print(f"{YELLOW}[1] Display System Information")
        print(f"{YELLOW}[2] List Running Processes")
        print(f"{MAGENTA}[0] Back to Main Menu{NC}")
        print(f"{BLUE}------------------------------{NC}")
        choice = input(f"{YELLOW}>>> Select System option [0-2]: {NC}")

        if choice == '1':
            display_system_info()
            pause_and_continue()
        elif choice == '2':
            list_running_processes()
            pause_and_continue()
        elif choice == '0':
            break
        else:
            print(f"{RED}Invalid choice.{NC}")
            pause_and_continue()



def main():
    while True:
        clear_screen()
        display_header()
        print(f"{MAGENTA}========= MAIN MENU ========={NC}")
        print(f"{YELLOW}[1] {GREEN}Cryptography Tools{NC}")
        print(f"{YELLOW}[2] {BLUE}Network Tools{NC}")
        print(f"{YELLOW}[3] {CYAN}Data Utilities{NC}")
        print(f"{YELLOW}[4] {WHITE}System Utilities{NC}")
        print(f"{YELLOW}[0] {RED}Exit EVIL LOCK{NC}")
        print(f"{MAGENTA}==========================={NC}")
        choice = input(f"{YELLOW}>>> Enter your choice [0-4]: {NC}")

        if choice == '1':
            handle_crypto_menu()
        elif choice == '2':
            handle_network_menu()
        elif choice == '3':
            handle_data_menu()
        elif choice == '4':
            handle_system_menu()
        elif choice == '0':
            clear_screen()
            print(ASCII_ART)
            print(f"\n{YELLOW}[*] Terminating EVIL LOCK Session... Stay safe!{NC}")
            sys.exit(0)
        else:
            print(f"{RED}Invalid choice. Please select between 0 and 4.{NC}")
            pause_and_continue()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{RED}[!] Operation interrupted by user. Exiting forcefully.{NC}")
        sys.exit(1)
    except Exception as e:

        print(f"\n{RED}[!!!] A CRITICAL UNEXPECTED ERROR OCCURRED: {e}{NC}")
        print(f"{RED}       Please report this issue if possible.{NC}")
        sys.exit(1)
