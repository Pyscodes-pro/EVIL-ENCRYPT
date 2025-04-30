import base64
import os
import sys
import platform # Needed for clear screen
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import InvalidToken
import getpass # For hiding password input

# --- ANSI Colors ---
GREEN = '\033[0;32m'
RED = '\033[0;31m'
CYAN = '\033[0;36m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m' # No Color

# --- ASCII Art ---
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
      EVIL LOCK TOOL  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{NC}"""

# --- Author Info ---
AUTHOR_INFO = f"""{GREEN}=============================================================={NC}
{YELLOW} Author    : {CYAN}Pyscodes-pro{NC}
{YELLOW} Instagram : {CYAN}https://instagram.com/pyscodes{NC}
{YELLOW} GitHub    : {CYAN}https://github.com/Pyscodes-pro{NC}
{GREEN}=============================================================={NC}"""

def clear_screen():
    """Clears the terminal screen."""
    command = 'cls' if platform.system().lower() == 'windows' else 'clear'
    os.system(command)

def display_header():
    """Displays the ASCII art and author info."""
    print(ASCII_ART)
    print(AUTHOR_INFO)
    print() # Add a newline for spacing

def generate_salt():
    return os.urandom(16)

def derive_key(password: bytes, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000, # NIST recommendation
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key

# --- Message Encryption/Decryption ---

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

# --- File Encryption/Decryption ---

def encrypt_file(password: str, input_filepath: str, output_filepath: str):
    try:
        salt = generate_salt()
        key = derive_key(password.encode(), salt)
        f = Fernet(key)

        with open(input_filepath, 'rb') as file:
            file_data = file.read()

        encrypted_data = f.encrypt(file_data)

        with open(output_filepath, 'wb') as file:
            file.write(salt) # Write salt first
            file.write(encrypted_data) # Then encrypted data
        return True
    except FileNotFoundError:
        print(f"{RED}[!] Encryption Error (File): Input file not found: '{input_filepath}'{NC}")
        return False
    except PermissionError:
        print(f"{RED}[!] Encryption Error (File): Permission denied to read '{input_filepath}' or write '{output_filepath}'.{NC}")
        return False
    except Exception as e:
        print(f"{RED}[!] Encryption Error (File): {e}{NC}")
        return False

def decrypt_file(password: str, input_filepath: str, output_filepath: str):
    try:
        with open(input_filepath, 'rb') as file:
            salt = file.read(16) # Read the salt (first 16 bytes)
            encrypted_data = file.read() # Read the rest of the data

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
        print(f"{RED}[!] Decryption Error (File): Permission denied to read '{input_filepath}' or write '{output_filepath}'.{NC}")
        return False
    except Exception as e:
        print(f"{RED}[!] Decryption Error (File): {e}{NC}")
        return False

# --- Menu and Main Logic ---

def display_menu():
    print(f"{BLUE}==================== OPTIONS ===================={NC}")
    print(f"{YELLOW}[1] {GREEN}Encrypt Text Message{NC}")
    print(f"{YELLOW}[2] {GREEN}Decrypt Text Message{NC}")
    print(f"{YELLOW}[3] {CYAN}Encrypt File{NC}")
    print(f"{YELLOW}[4] {CYAN}Decrypt File{NC}")
    print(f"{YELLOW}[5] {RED}Exit Secure Session{NC}")
    print(f"{BLUE}================================================={NC}")

def get_password(prompt=f"{CYAN}Enter secret key (input hidden): {NC}"):
    """Gets password securely without echoing."""
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


def main():
    while True:
        clear_screen()
        display_header()
        display_menu()
        choice = input(f"{YELLOW}>>> Enter your choice [1-5]: {NC}")

        if choice == '1': # Encrypt Message
            password = get_password()
            if not password: continue
            message = input(f"{CYAN}Enter the message to encrypt: {NC}")
            if not message:
                print(f"{RED}[!] Message cannot be empty.{NC}")
                input(f"\n{YELLOW}Press Enter to continue...{NC}")
                continue
            print(f"\n{YELLOW}[*] Encrypting message... Standby.{NC}")
            encrypted = encrypt_message(password, message)
            if encrypted:
                print(f"{GREEN}[+] Message Encryption Successful!{NC}")
                print(f"{CYAN}--- Ciphertext (Salt Included) ---{NC}")
                print(f"{GREEN}{encrypted}{NC}")
                print(f"{CYAN}------------------------------------{NC}")

        elif choice == '2': # Decrypt Message
            password = get_password()
            if not password: continue
            encrypted_data = input(f"{CYAN}Enter the ciphertext (including salt): {NC}")
            if not encrypted_data:
                print(f"{RED}[!] Ciphertext cannot be empty.{NC}")
                input(f"\n{YELLOW}Press Enter to continue...{NC}")
                continue
            print(f"\n{YELLOW}[*] Decrypting message... Standby.{NC}")
            decrypted = decrypt_message(password, encrypted_data)
            if decrypted:
                print(f"{GREEN}[+] Message Decryption Successful!{NC}")
                print(f"{CYAN}--- Plaintext ---{NC}")
                print(f"{GREEN}{decrypted}{NC}")
                print(f"{CYAN}-----------------{NC}")

        elif choice == '3': # Encrypt File
            password = get_password()
            if not password: continue
            input_file = input(f"{CYAN}Enter the path to the file to encrypt: {NC}")
            default_output = f"{input_file}.enc"
            output_file = input(f"{CYAN}Enter the desired output path (default: {default_output}): {NC}") or default_output

            if not os.path.exists(input_file):
                 print(f"{RED}[!] Input file not found: '{input_file}'{NC}")
                 input(f"\n{YELLOW}Press Enter to continue...{NC}")
                 continue
            if os.path.abspath(input_file) == os.path.abspath(output_file):
                 print(f"{RED}[!] Input and output file cannot be the same.{NC}")
                 input(f"\n{YELLOW}Press Enter to continue...{NC}")
                 continue

            print(f"\n{YELLOW}[*] Encrypting file '{os.path.basename(input_file)}'... Standby.{NC}")
            success = encrypt_file(password, input_file, output_file)
            if success:
                print(f"{GREEN}[+] File Encryption Successful!{NC}")
                print(f"{GREEN}   Input : {input_file}{NC}")
                print(f"{GREEN}   Output: {output_file}{NC}")

        elif choice == '4': # Decrypt File
            password = get_password()
            if not password: continue
            input_file = input(f"{CYAN}Enter the path to the file to decrypt (.enc): {NC}")
            default_output = input_file.replace('.enc', '.dec') if input_file.endswith('.enc') else f"{input_file}.dec"
            output_file = input(f"{CYAN}Enter the desired output path (default: {default_output}): {NC}") or default_output

            if not os.path.exists(input_file):
                 print(f"{RED}[!] Input file not found: '{input_file}'{NC}")
                 input(f"\n{YELLOW}Press Enter to continue...{NC}")
                 continue
            if os.path.abspath(input_file) == os.path.abspath(output_file):
                 print(f"{RED}[!] Input and output file cannot be the same.{NC}")
                 input(f"\n{YELLOW}Press Enter to continue...{NC}")
                 continue

            print(f"\n{YELLOW}[*] Decrypting file '{os.path.basename(input_file)}'... Standby.{NC}")
            success = decrypt_file(password, input_file, output_file)
            if success:
                print(f"{GREEN}[+] File Decryption Successful!{NC}")
                print(f"{GREEN}   Input : {input_file}{NC}")
                print(f"{GREEN}   Output: {output_file}{NC}")

        elif choice == '5': # Exit
            clear_screen()
            print(ASCII_ART) # Show art one last time on exit maybe?
            print(f"\n{YELLOW}[*] Terminating Secure Session... Goodbye!{NC}")
            sys.exit(0)

        else:
            print(f"{RED}[!] Invalid choice. Please select between 1 and 5.{NC}")

        input(f"\n{YELLOW}Press Enter to return to the main menu...{NC}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{RED}[!] Operation interrupted by user. Exiting forcefully.{NC}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{RED}[!] An unexpected critical error occurred: {e}{NC}")
        sys.exit(1)
