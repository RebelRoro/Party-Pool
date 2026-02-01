"""
Party Pool - Main entry point
Multi-mode launcher for Server, Client, and Root Administrator interfaces
"""

import os
import sys
import time
import shutil
import zipfile
import getpass

import config
from util import clear_screen, print_info, print_success, print_error, print_warning
from util.common import decrypt_ip, get_local_ip


def display_menu():
    """Display main menu."""
    clear_screen()
    menu = """
    ╔════════════════════════════════════════════════════════════════╗
    ║                                                                ║
    ║                  🎉 PARTY POOL SERVER 🎉                       ║
    ║                                                                ║
    ║                 Multi-Mode Chat Application                    ║
    ║                                                                ║
    ╚════════════════════════════════════════════════════════════════╝

Please select an option:

  [1] 🖥️  Start Server
      - Start the Party Pool chat server on this machine
      
  [2] 📦 Generate Distribution Packages
      - Create shareable packages for clients and root users
      - Windows: Standalone EXE files
      - Linux/Mac: ZIP packages with all necessary files
      
  [3] 🔐 Login as Administrator (Root)
      - Access server control panel with admin privileges
  
  [4] 💬 Login as Client
      - Connect to the Party Pool chat server as a user
      
  [5] ❌ Exit
      - Close this application

════════════════════════════════════════════════════════════════
    """
    print(menu)


def display_distribution_menu():
    """Display distribution package generation menu."""
    clear_screen()
    menu = """
    ╔════════════════════════════════════════════════════════════════╗
    ║                                                                ║
    ║            📦 DISTRIBUTION PACKAGE GENERATOR 📦                ║
    ║                                                                ║
    ╚════════════════════════════════════════════════════════════════╝

Select package type to generate:

  [1] 💬 Client Package Only
      - For users who want to chat
      
  [2] 🔐 Root/Admin Package Only
      - For administrators who need server control
      
  [3] 📦 Both Client & Root Packages
      - Generate both packages at once
      
  [4] 🔙 Back to Main Menu

════════════════════════════════════════════════════════════════
    """
    print(menu)


def display_choose_os():
    """Choose operating system for package generation."""
    clear_screen()
    menu = """
    ╔════════════════════════════════════════════════════════════════╗
    ║                                                                ║
    ║                 🖥️ SELECT OPERATING SYSTEM 🖥️                  ║
    ║                                                                ║
    ╚════════════════════════════════════════════════════════════════╝

Select target operating system:

  [1] 🪟 Windows
      - Generates standalone EXE files using PyInstaller
        
  [2] 🐧 Linux/macOS
      - Generates ZIP packages with setup scripts
  
  [3] 📦 Both
      - Generates both packages at once
        
  [4] 🔙 Back to Main Menu

════════════════════════════════════════════════════════════════
    """
    print(menu)
    

def ensure_encrypted_ip():
    """Ensure encrypted IP file exists and is bound to this server's IP."""
    from util.encrypt import init_encrypt
    
    # Check if file doesn't exist or is empty
    if not os.path.exists(config.ENCRYPTED_IP_FILE) or not open(config.ENCRYPTED_IP_FILE, "r", encoding="utf-8").read().strip():
        print_warning("No encrypted IP found or file is empty. Creating now...")
        encrypted_ip = init_encrypt()
        with open(config.ENCRYPTED_IP_FILE, "w", encoding="utf-8") as f:
            f.write(encrypted_ip)
        print_success("Encrypted IP created and saved.")
        input("Press Enter to continue...")
        return True
    
    # File exists and has content - verify it matches server IP
    with open(config.ENCRYPTED_IP_FILE, "r", encoding="utf-8") as f:
        encrypted_ip = f.read().strip()
    
    server_ip = get_local_ip()
    print_info(f"Server IP detected: {server_ip}")
    print_info("Enter passkey to verify encrypted IP binding...")
    passkey = getpass.getpass("Passkey: ").strip()
    
    try:
        decrypted_ip = decrypt_ip(encrypted_ip, passkey)
        
        if decrypted_ip == server_ip:
            print_success(f"Encrypted IP is bound to this server ({server_ip}). Press Enter to continue...")
            input()
            return True
        else:
            print_error(f"IP mismatch! Encrypted IP ({decrypted_ip}) does not match server IP ({server_ip}).")
            print_warning("Choose an option:")
            print("  [1] Overwrite existing encrypted IP with new one")
            print("  [2] Backup old IP to .bak file and create new encrypted IP")
            print("  [3] Continue without changes (may cause connection issues)")
            print("  [4] Re-enter passkey to try again")
            print("  [5] Cancel and return to menu")
            
            choice = input("Enter choice (1-5): ").strip()
            
            if choice == "1":
                print_warning("Overwriting encrypted IP...")
                encrypted_ip = init_encrypt()
                with open(config.ENCRYPTED_IP_FILE, "w", encoding="utf-8") as f:
                    f.write(encrypted_ip)
                print_success("Encrypted IP overwritten successfully.")
                input("Press Enter to continue...")
                return True
            
            elif choice == "2":
                backup_file = config.ENCRYPTED_IP_FILE + ".bak"
                print_warning(f"Backing up old IP to {backup_file}...")
                shutil.copy(config.ENCRYPTED_IP_FILE, backup_file)
                print_success("Backup created.")
                
                encrypted_ip = init_encrypt()
                with open(config.ENCRYPTED_IP_FILE, "w", encoding="utf-8") as f:
                    f.write(encrypted_ip)
                print_success("New encrypted IP created successfully.")
                input("Press Enter to continue...")
                return True
            
            elif choice == "3":
                print_error("Are you sure you want to continue without changes? This may cause connection issues.")
                conf = input("Yes[Y]/No[N]: ").strip().lower()
                if conf == "y":
                    return True
                else:
                    return ensure_encrypted_ip()
            
            elif choice == "4":
                return ensure_encrypted_ip()
            
            elif choice == "5":
                print_info("Operation cancelled. Returning to menu...")
                return False
            
            else:
                print_info("Invalid choice. Returning to menu...")
                return False
                
    except Exception as e:
        print_error(f"Failed to decrypt IP (wrong passkey?): {e}")
        print_warning("Choose an option:")
        print("  [1] Overwrite existing encrypted IP with new one")
        print("  [2] Backup old IP to .bak file and create new encrypted IP")
        print("  [3] Continue without changes (may cause connection issues)")
        print("  [4] Re-enter passkey to try again")
        print("  [5] Cancel and return to menu")
        
        choice = input("Enter choice (1-5): ").strip()
        
        if choice == "1":
            print_warning("Overwriting encrypted IP...")
            encrypted_ip = init_encrypt()
            with open(config.ENCRYPTED_IP_FILE, "w", encoding="utf-8") as f:
                f.write(encrypted_ip)
            print_success("Encrypted IP overwritten successfully.")
            input("Press Enter to continue...")
            return True
        
        elif choice == "2":
            backup_file = config.ENCRYPTED_IP_FILE + ".bak"
            print_warning(f"Backing up old IP to {backup_file}...")
            shutil.copy(config.ENCRYPTED_IP_FILE, backup_file)
            print_success("Backup created.")
            
            encrypted_ip = init_encrypt()
            with open(config.ENCRYPTED_IP_FILE, "w", encoding="utf-8") as f:
                f.write(encrypted_ip)
            print_success("New encrypted IP created successfully.")
            input("Press Enter to continue...")
            return True
        
        elif choice == "3":
            print_error("Are you sure you want to continue without changes? This may cause connection issues.")
            conf = input("Yes[Y]/No[N]: ").strip().lower()
            if conf == "y":
                return True
            else:
                return ensure_encrypted_ip()
        
        elif choice == "4":
            return ensure_encrypted_ip()
        
        elif choice == "5":
            print_info("Operation cancelled. Returning to menu...")
            return False
        
        else:
            print_info("Invalid choice. Returning to menu...")
            return False


def create_client_requirements():
    """Create minimal requirements for client."""
    return """# Party Pool Client Requirements
colorama>=0.4.6
cryptography>=41.0.0
prompt-toolkit>=3.0.0
"""


def create_root_requirements():
    """Create minimal requirements for root."""
    return """# Party Pool Root Requirements
colorama>=0.4.6
cryptography>=41.0.0
prompt-toolkit>=3.0.0
"""


def create_client_setup_bat():
    """Create Windows setup script for client."""
    return """@echo off
REM Party Pool Client Setup - Windows
echo.
echo ====================================================
echo        Party Pool Client - Windows Setup
echo ====================================================
echo.

python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: Python is not installed.
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Setup complete! Run 'python client.py' to connect.
pause
"""


def create_client_setup_sh():
    """Create Linux/Mac setup script for client."""
    return """#!/bin/bash
# Party Pool Client Setup - Linux/macOS
echo ""
echo "===================================================="
echo "      Party Pool Client - Linux/macOS Setup"
echo "===================================================="
echo ""

if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    exit 1
fi

echo "Installing dependencies..."
pip3 install -r requirements.txt

echo ""
echo "Setup complete! Run 'python3 client.py' to connect."
"""


def create_root_setup_bat():
    """Create Windows setup script for root."""
    return """@echo off
REM Party Pool Root Setup - Windows
echo.
echo ====================================================
echo        Party Pool Root/Admin - Windows Setup
echo ====================================================
echo.

python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: Python is not installed.
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Setup complete! Run 'python root.py' to connect as admin.
pause
"""


def create_root_setup_sh():
    """Create Linux/Mac setup script for root."""
    return """#!/bin/bash
# Party Pool Root Setup - Linux/macOS
echo ""
echo "===================================================="
echo "      Party Pool Root/Admin - Linux/macOS Setup"
echo "===================================================="
echo ""

if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    exit 1
fi

echo "Installing dependencies..."
pip3 install -r requirements.txt

echo ""
echo "Setup complete! Run 'python3 root.py' to connect as admin."
"""


def create_standalone_client_py():
    """Create a standalone client.py with embedded utilities."""
    with open(config.ENCRYPTED_IP_FILE, "r", encoding="utf-8") as f:
        encrypted_ip = f.read().strip()
    
    standalone = f'''"""
Party Pool Client - Standalone Version
Connect to Party Pool chat server.
"""

import base64
import socket
import threading
import asyncio
import getpass
import time
import sys
import os
import hmac
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.shortcuts import print_formatted_text
from prompt_toolkit.formatted_text import HTML
from colorama import Fore, Style, init

init(autoreset=True)

# ==================== CONFIGURATION ====================
SERVER_PORT = {config.SERVER_PORT}
BUFFER_SIZE = {config.BUFFER_SIZE}
AUTH_MESSAGE = {config.AUTH_MESSAGE}
KDF_ITERATIONS = {config.KDF_ITERATIONS}
ILLEGAL_CHARS = {config.ILLEGAL_CHARS}
ENCRYPTED_IP = "{encrypted_ip}"

# ==================== UTILITIES ====================

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def slow_type(text, delay=0.05):
    for char in text:
        sys.stdout.write(Fore.CYAN + char)
        sys.stdout.flush()
        time.sleep(delay)
    print(Style.RESET_ALL)

def print_success(msg):
    print(Fore.GREEN + "\\n✓ " + msg + Style.RESET_ALL)

def print_error(msg):
    print(Fore.RED + "\\n✗ " + msg + Style.RESET_ALL)

def print_info(msg):
    print(Fore.CYAN + "\\nℹ  " + msg + Style.RESET_ALL)

def print_warning(msg):
    print(Fore.YELLOW + "\\n⚠  " + msg + Style.RESET_ALL)

def derive_fernet_key(password, salt, iterations=KDF_ITERATIONS):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def decrypt_ip(compound, password):
    salt_b64, token_b64 = compound.split("|", 1)
    salt = base64.urlsafe_b64decode(salt_b64)
    token = base64.urlsafe_b64decode(token_b64)
    key = derive_fernet_key(password, salt)
    f = Fernet(key)
    return f.decrypt(token).decode()

def compute_hmac(secret, message):
    return hmac.new(secret.encode(), message, hashlib.sha256).digest()

# ==================== CLIENT CODE ====================

client_socket = None
u_name = None

def display_banner():
    clear_screen()
    slow_type("Connecting to Party Pool...", delay=0.06)
    time.sleep(0.5)
    clear_screen()
    
    banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║          🎉 PARTY POOL - Chat Server 🎉                   ║
║                                                           ║
║        Where messages flow and fun begins!                ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

💬 Connected and Ready!
📝 Type /help for available commands
📝 Press Ctrl+D/Ctrl+C to exit
    """
    print(banner)

def display_help():
    print_formatted_text(HTML('<b>╔══════════════════════════════════════════════════════════╗</b>'))
    print_formatted_text(HTML('<b>║                  📋 AVAILABLE COMMANDS 📋                ║</b>'))
    print_formatted_text(HTML('<b>╠══════════════════════════════════════════════════════════╣</b>'))
    print_formatted_text(HTML('<b>║ <ansicyan>/help</ansicyan>              - Show this help message              ║</b>'))
    print_formatted_text(HTML('<b>║ <ansicyan>/online</ansicyan>            - Show online users                   ║</b>'))
    print_formatted_text(HTML('<b>║ <ansicyan>/ip</ansicyan>                - Show your IP address                ║</b>'))
    print_formatted_text(HTML('<b>║ <ansicyan>/request [msg]</ansicyan>     - Send a request to server admin      ║</b>'))
    print_formatted_text(HTML('<b>║ <ansicyan>/exit</ansicyan>              - Exit Party Pool                     ║</b>'))
    print_formatted_text(HTML('<b>╚══════════════════════════════════════════════════════════╝</b>'))

def display_online_users(message):
    data = message.replace("ONLINE_USERS:", "")
    if data == "No users online":
        print_formatted_text(HTML('<ansiyellow>No users currently online.</ansiyellow>'))
        return
    users = data.split("|")
    print_formatted_text(HTML('<b>╔══════════════════════════════════════════╗</b>'))
    print_formatted_text(HTML('<b>║             👥 ONLINE USERS 👥           ║</b>'))
    print_formatted_text(HTML('<b>╠══════════════════════════════════════════╣</b>'))
    for user_data in users:
        parts = user_data.split(":", 1)
        if len(parts) == 2:
            color, username = parts
            padded = username.center(40)
            print_formatted_text(HTML(f'<b>║ <{{color}}>{{padded}}</{{color}}> ║</b>'))
    print_formatted_text(HTML('<b>╚══════════════════════════════════════════╝</b>'))

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(BUFFER_SIZE).decode('utf-8')
            if message:
                if message.startswith("ONLINE_USERS:"):
                    display_online_users(message)
                elif message.startswith("YOUR_IP:"):
                    ip = message.replace("YOUR_IP:", "")
                    print_formatted_text(HTML(f'<b><ansicyan>Your IP address: </ansicyan><ansigreen>{{ip}}</ansigreen></b>'))
                elif message.startswith("REQUEST_OK"):
                    print_formatted_text(HTML('<b><ansigreen>✓ Your request has been submitted to the server admin.</ansigreen></b>'))
                elif message.startswith("REQUEST_FAIL"):
                    print_formatted_text(HTML('<b><ansired>✗ Failed to submit request. Please try again.</ansired></b>'))
                elif "------------------------WELCOME" in message:
                    print_formatted_text(HTML(f'<b><ansigreen>{{message}}</ansigreen></b>'))
                elif "------------------------GOOD BYE" in message:
                    print_formatted_text(HTML(f'<b><ansired>{{message}}</ansired></b>'))
                elif "$root@party-pool:" in message:
                    print_formatted_text(HTML(f"<b><ansired>{{message}}</ansired></b>"))
                else:
                    print_formatted_text(HTML(f'<b><ansicyan>{{message}}</ansicyan></b>'))
        except Exception as e:
            print_formatted_text(HTML(f'<b><ansired>Connection lost. Exiting...</ansired></b>'))
            sys.stdout.flush()
            time.sleep(5)
            clear_screen()
            os._exit(0)

def handle_client_command(message):
    cmd = message.strip().lower()
    if cmd == '/help':
        display_help()
        return True
    elif cmd == '/exit':
        print_formatted_text(HTML(f'<b><ansiyellow>Disconnecting from Party Pool...</ansiyellow></b>'))
        sys.stdout.flush()
        time.sleep(2)
        clear_screen()
        os._exit(0)
    return False

def validate_message(message):
    """Validate message before sending."""
    if not message.strip():
        print_error("Cannot send empty message.")
        return False
    if any(char in message for char in ILLEGAL_CHARS):
        print_error(f"Message contains illegal characters: [{{', '.join(ILLEGAL_CHARS)}}]")
        return False
    return True

async def send_messages_loop(session, client_socket):
    global u_name
    print_formatted_text(HTML(f"<ansicyan>Connected as: {{u_name}}</ansicyan> "))
    
    while True:
        try:
            message = await session.prompt_async(f"${{u_name}}: ")
            if validate_message(message):
                if handle_client_command(message):
                    continue
                client_socket.send(message.encode('utf-8'))
        except (EOFError, KeyboardInterrupt):
            print_formatted_text(HTML(f'<ansired>Exiting...</ansired>'))
            sys.stdout.flush()
            time.sleep(2)
            clear_screen()
            os._exit(0)
        except Exception as e:
            print_formatted_text(HTML(f'<ansired>Error: {{e}}</ansired>'))
            sys.stdout.flush()
            time.sleep(5)
            clear_screen()
            os._exit(0)

def start_client():
    global client_socket, u_name
    
    print_info("Enter passkey to connect to server: ")
    passwd = getpass.getpass("").strip()
    
    try:
        server_ip = decrypt_ip(ENCRYPTED_IP, passwd)
    except Exception as e:
        print_error("Connection failed: Wrong passkey or corrupted IP address.")
        sys.stdout.flush()
        time.sleep(5)
        return
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect((server_ip, SERVER_PORT))
        
        auth_token = compute_hmac(passwd, AUTH_MESSAGE)
        client_socket.send(len(auth_token).to_bytes(2, "big") + auth_token)
        
        duplicate_client = client_socket.recv(64)
        if duplicate_client == b'YES-IP':
            print_error("A session already exists from this machine.")
            sys.stdout.flush()
            time.sleep(5)
            client_socket.close()
            return
        
        reply = client_socket.recv(64)
        
        if reply == b"OK":
            print_success("Authenticated successfully!")
            time.sleep(2)
            display_banner()
            
            while True:
                print_info("Enter your username (no spaces, not 'root'): ")
                u_name = input().strip().replace(" ", "")
                if not u_name:
                    print_error("Username cannot be empty. Try again.")
                    continue
                client_socket.send(u_name.encode('utf-8'))
                username_response = client_socket.recv(64)
                if username_response == b'YES-U':
                    print_error("Username already exists or is invalid. Try another.")
                    continue
                else:
                    break
            
            thread_receive = threading.Thread(target=receive_messages, args=(client_socket,), daemon=True)
            thread_receive.start()
            
            with patch_stdout():
                session = PromptSession()
                asyncio.run(send_messages_loop(session, client_socket))
        else:
            print_error("Authentication failed. Check your passkey.")
            time.sleep(5)
            client_socket.close()
            return
    
    except Exception as e:
        print_error(f'Connection Error: {{e}}')
        sys.stdout.flush()
        time.sleep(5)
    
    finally:
        if client_socket:
            client_socket.close()

if __name__ == "__main__":
    start_client()
'''
    return standalone


def create_standalone_root_py():
    """Create a standalone root.py with embedded utilities."""
    with open(config.ENCRYPTED_IP_FILE, "r", encoding="utf-8") as f:
        encrypted_ip = f.read().strip()
    
    standalone = f'''"""
Party Pool Root - Standalone Admin Version
Administrative control interface for Party Pool server.
"""

import base64
import socket
import asyncio
import getpass
import time
import sys
import os
import threading
import pickle as pkl
import hmac
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from prompt_toolkit.shortcuts import print_formatted_text
from prompt_toolkit.formatted_text import HTML
from colorama import Fore, Style, init

init(autoreset=True)

# ==================== CONFIGURATION ====================
SERVER_PORT = {config.SERVER_PORT}
BUFFER_SIZE = {config.BUFFER_SIZE}
ROOT_AUTH = {config.ROOT_AUTH}
KDF_ITERATIONS = {config.KDF_ITERATIONS}
ENCRYPTED_IP = "{encrypted_ip}"

# ==================== UTILITIES ====================

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def slow_type(text, delay=0.05):
    for char in text:
        sys.stdout.write(Fore.RED + char)
        sys.stdout.flush()
        time.sleep(delay)
    print(Style.RESET_ALL)

def print_success(msg):
    print(Fore.GREEN + "\\n✓ " + msg + Style.RESET_ALL)

def print_error(msg):
    print(Fore.RED + "\\n✗ " + msg + Style.RESET_ALL)

def print_info(msg):
    print(Fore.CYAN + "\\nℹ  " + msg + Style.RESET_ALL)

def print_warning(msg):
    print(Fore.YELLOW + "\\n⚠  " + msg + Style.RESET_ALL)

def derive_fernet_key(password, salt, iterations=KDF_ITERATIONS):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def decrypt_ip(compound, password):
    salt_b64, token_b64 = compound.split("|", 1)
    salt = base64.urlsafe_b64decode(salt_b64)
    token = base64.urlsafe_b64decode(token_b64)
    key = derive_fernet_key(password, salt)
    f = Fernet(key)
    return f.decrypt(token).decode()

def compute_hmac(secret, message):
    return hmac.new(secret.encode(), message, hashlib.sha256).digest()

# ==================== ROOT CODE ====================

root_socket = None

def display_banner():
    clear_screen()
    slow_type("Logging in as root...", delay=0.08)
    time.sleep(2)
    clear_screen()
    
    banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║      ⚙️  PARTY POOL - ROOT CONTROL PANEL ⚙️               ║
║                                                           ║
║        Administrative Control Interface                   ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

🔑 Logged in as root with full privileges
📋 Type 'list' for available commands
⚠️ Press Ctrl+C to exit
    """
    print(banner)

def display_list():
    print_formatted_text(HTML('<b>╔═════════════════════════════════════════════════════════════════════════════════════════════════════╗</b>'))
    print_formatted_text(HTML('<b>║                                       📋 ROOT COMMANDS 📋                                           ║</b>'))
    print_formatted_text(HTML('<b>╠═════════════════════════════════════════════════════════════════════════════════════════════════════╣</b>'))
    print_formatted_text(HTML('<b>║ <ansicyan>list</ansicyan>                              │ Lists all available commands                                    ║</b>'))
    print_formatted_text(HTML('<b>║ <ansicyan>close-server [-t &lt;t&gt;] [-m "msg"]</ansicyan>  │ Closes the server [after t seconds] [with reason message]       ║</b>'))
    print_formatted_text(HTML('<b>║ <ansicyan>list-conn [-ip | -u]</ansicyan>              │ Lists active connections [only IPs | only usernames]            ║</b>'))
    print_formatted_text(HTML('<b>║ <ansicyan>remove [-ip &lt;ip&gt; | -u &lt;u&gt;]</ansicyan>        │ Removes the provided IP address or username from connections    ║</b>'))
    print_formatted_text(HTML('<b>║ <ansicyan>send [-all | -ip &lt;ip(s)&gt;] ["msg"]</ansicyan> │ Broadcasts message to all clients or to the given IP addresses  ║</b>'))
    print_formatted_text(HTML('<b>║ <ansicyan>exit</ansicyan>                              │ Logout from root                                                ║</b>'))
    print_formatted_text(HTML('<b>╚═════════════════════════════════════════════════════════════════════════════════════════════════════╝</b>'))

def receive_messages(root_socket):
    while True:
        try:
            message = pkl.loads(root_socket.recv(2048))
            if message:
                print(message)
        except:
            continue

def handle_local_command(cmd):
    cmd_lower = cmd.strip().lower()
    if cmd_lower == 'list' or cmd_lower == 'help':
        display_list()
        return True
    elif cmd_lower == 'clear' or cmd_lower == 'cls':
        clear_screen()
        return True
    elif cmd_lower == 'exit':
        print_warning("Logging out from root...")
        sys.stdout.flush()
        time.sleep(2)
        clear_screen()
        os._exit(0)
    return False

async def send_command():
    global root_socket
    
    while True:
        try:
            print_formatted_text(HTML(f"<ansired>$root@party-pool:</ansired> "), end="")
            cmd = await asyncio.to_thread(input)
            
            if not cmd or not cmd.strip():
                continue
            
            if handle_local_command(cmd):
                continue
            
            if root_socket:
                root_socket.send(cmd.encode('utf-8'))
                cmd_exe = root_socket.recv(64)
            else:
                print_error("Not connected to server.")
                continue
            
            if cmd_exe == b'OK':
                print_success("Command executed successfully.\\n")
            elif cmd_exe == b'FAIL':
                print_error("Command failed.\\n")
        except pkl.UnpicklingError:
            continue
        except KeyboardInterrupt:
            print_error('Interrupted. Exiting...')
            sys.stdout.flush()
            time.sleep(2)
            clear_screen()
            os._exit(0)
        except Exception as e:
            print_error("Server connection lost.")
            sys.stdout.flush()
            time.sleep(2)
            clear_screen()
            os._exit(0)

def handle_root():
    global root_socket
    try:
        thread_receive = threading.Thread(target=receive_messages, args=(root_socket,), daemon=True)
        thread_receive.start()
        asyncio.run(send_command())
    except KeyboardInterrupt:
        print_error('Interrupted. Exiting...')
        sys.stdout.flush()
        time.sleep(2)
        clear_screen()
        os._exit(0)
    except Exception as e:
        print_error(f"Error: {{e}}")
        return

def init_root():
    global root_socket
    
    print_info("Enter the server passkey (same as client passkey): ")
    passkey = getpass.getpass("").strip()
    
    print_info("Enter root password: ")
    root_passwd = getpass.getpass("").strip()
    
    try:
        server_ip = decrypt_ip(ENCRYPTED_IP, passkey)
    except Exception as e:
        print_error("Connection failed: Wrong passkey or corrupted IP address.")
        sys.stdout.flush()
        time.sleep(5)
        return
    
    root_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        root_socket.connect((server_ip, SERVER_PORT))
        
        auth_token = compute_hmac(root_passwd, ROOT_AUTH)
        root_socket.send(len(auth_token).to_bytes(2, "big") + auth_token)
        
        reply = root_socket.recv(64)
        
        if reply == b'ROOT-OK':
            print_success("Logged in as root with full privileges!")
            time.sleep(5)
            display_banner()
            handle_root()
        else:
            print_error("Server refused connection. Root login may already be active or password is incorrect.")
            sys.stdout.flush()
            time.sleep(5)
            root_socket.close()
            return
    
    except Exception as e:
        print_error(f'Connection Error: {{e}}')
        sys.stdout.flush()
        time.sleep(5)
    
    finally:
        if root_socket:
            root_socket.close()

if __name__ == "__main__":
    init_root()
'''
    return standalone


# Global flag to track if encrypted IP has been validated this session
_encrypted_ip_validated = False


def check_existing_package(file_path, package_name):
    """Check if package exists and ask for overwrite confirmation.
    Returns True if we can proceed (file doesn't exist or user confirmed overwrite).
    Returns False if user denied overwrite.
    """
    if os.path.exists(file_path):
        print_warning(f"Package '{package_name}' already exists!")
        choice = input("Overwrite existing package? [Y/N]: ").strip().lower()
        if choice != 'y':
            print_info("Skipping package creation...")
            return False
        print_info("Overwriting existing package...")
    return True


def cleanup_failed_dist(dist_dir, package_type):
    """Clean up dist folder after failed package generation."""
    try:
        if os.path.exists(dist_dir):
            shutil.rmtree(dist_dir, ignore_errors=True)
            print_info(f"Removed corrupted {package_type} packages.")
    except Exception as e:
        print_warning(f"Could not clean up dist folder: {e}")


def generate_client_package(skip_ip_check=False):
    """Generate client distribution package."""
    global _encrypted_ip_validated
    
    if not skip_ip_check and not _encrypted_ip_validated:
        if not ensure_encrypted_ip():
            return False
        _encrypted_ip_validated = True
    
    dist_dir = os.path.join("dist", "client")
    os.makedirs(dist_dir, exist_ok=True)
    
    # Version-suffixed package name
    version = config.APP_VERSION
    exe_name = f"{config.CLIENT_EXE_NAME}-v{version}"
    exe_path = os.path.join(dist_dir, f"{exe_name}.exe")
    
    # Check for existing package
    if not check_existing_package(exe_path, f"{exe_name}.exe"):
        return False
    
    print_info("Generating Windows client executable...")
    try:
        import PyInstaller.__main__ as PyInstall
        
        standalone_path = os.path.join(dist_dir, "client_standalone.py")
        with open(standalone_path, "w", encoding="utf-8") as f:
            f.write(create_standalone_client_py())
        PyInstall.run([
            standalone_path,
            '--onefile',
            f'--name={exe_name}',
            f'--distpath={dist_dir}',
            f'--icon={config.CLIENT_ICON_FILE}',
            '--clean',
        ])
        os.remove(standalone_path)
        if os.path.exists("build"):
            shutil.rmtree("build", ignore_errors=True)
        spec_file = f"{exe_name}.spec"
        if os.path.exists(spec_file):
            os.remove(spec_file)
        
        if not os.path.exists(exe_path):
            raise Exception("EXE file was not created")
        
        print_success(f"Client EXE created: {os.path.abspath(exe_path)}")
        
    except ImportError:
        print_warning("PyInstaller not found. Creating ZIP package instead...")
        return generate_client_zip(skip_ip_check=True)
    except Exception as e:
        print_error(f"Failed to generate client package: {e}")        
        # cleanup_failed_dist(dist_dir, "client")
        return False
    
    return True


def generate_client_zip(skip_ip_check=False):
    """Generate client ZIP package for cross-platform distribution."""
    global _encrypted_ip_validated
    
    if not skip_ip_check and not _encrypted_ip_validated:
        if not ensure_encrypted_ip():
            return False
        _encrypted_ip_validated = True
    
    dist_dir = os.path.join("dist", "client")
    os.makedirs(dist_dir, exist_ok=True)
    
    # Version-suffixed package name
    version = config.APP_VERSION
    zip_name = f"PartyPoolClient-v{version}.zip"
    zip_path = os.path.join(dist_dir, zip_name)
    
    # Check for existing package
    if not check_existing_package(zip_path, zip_name):
        return False
    
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("client.py", create_standalone_client_py())
            zf.writestr("requirements.txt", create_client_requirements())
            zf.writestr("setup.bat", create_client_setup_bat())
            zf.writestr("setup.sh", create_client_setup_sh())
            zf.writestr("README.txt", """Party Pool Client
=================

Setup Instructions:
-------------------
Windows: Run setup.bat, then run 'python client.py'
Linux/Mac: Run 'chmod +x setup.sh && ./setup.sh', then run 'python3 client.py'

Usage:
------
1. Run the client (python client.py)
2. Enter the passkey provided by the server administrator
3. Enter your username when prompted
4. Start chatting!

Press Ctrl+C or Ctrl+D to exit.
""")
        
        print_success(f"Client ZIP created: {os.path.abspath(zip_path)}")
        return True
        
    except Exception as e:
        print_error(f"Failed to generate client ZIP: {e}")
        cleanup_failed_dist(dist_dir, "client")
        return False


def generate_root_package(skip_ip_check=False):
    """Generate root/admin distribution package."""
    global _encrypted_ip_validated
    
    if not skip_ip_check and not _encrypted_ip_validated:
        if not ensure_encrypted_ip():
            return False
        _encrypted_ip_validated = True
    
    dist_dir = os.path.join("dist", "root")
    os.makedirs(dist_dir, exist_ok=True)
    
    # Version-suffixed package name
    version = config.APP_VERSION
    exe_name = f"{config.ROOT_EXE_NAME}-v{version}"
    exe_path = os.path.join(dist_dir, f"{exe_name}.exe")
    
    # Check for existing package
    if not check_existing_package(exe_path, f"{exe_name}.exe"):
        return False
    
    print_info("Generating Windows root executable...")
    try:
        import PyInstaller.__main__ as PyInstall
        
        standalone_path = os.path.join(dist_dir, "root_standalone.py")
        with open(standalone_path, "w", encoding="utf-8") as f:
            f.write(create_standalone_root_py())
        
        PyInstall.run([
            standalone_path,
            '--onefile',
            f'--name={exe_name}',
            f'--distpath={dist_dir}',
            f'--icon={config.ROOT_ICON_FILE}',
            '--clean',
        ])
        
        os.remove(standalone_path)
        if os.path.exists("build"):
            shutil.rmtree("build", ignore_errors=True)
        spec_file = f"{exe_name}.spec"
        if os.path.exists(spec_file):
            os.remove(spec_file)
        
        if not os.path.exists(exe_path):
            raise Exception("EXE file was not created")
        
        print_success(f"Root EXE created: {os.path.abspath(exe_path)}")
        
    except ImportError:
        print_warning("PyInstaller not found. Creating ZIP package instead...")
        return generate_root_zip(skip_ip_check=True)
    except Exception as e:
        print_error(f"Failed to generate root package: {e}")
        cleanup_failed_dist(dist_dir, "root")
        return False
    
    return True


def generate_root_zip(skip_ip_check=False):
    """Generate root ZIP package for cross-platform distribution."""
    global _encrypted_ip_validated
    
    if not skip_ip_check and not _encrypted_ip_validated:
        if not ensure_encrypted_ip():
            return False
        _encrypted_ip_validated = True
    
    dist_dir = os.path.join("dist", "root")
    os.makedirs(dist_dir, exist_ok=True)
    
    # Version-suffixed package name
    version = config.APP_VERSION
    zip_name = f"PartyPoolRoot-v{version}.zip"
    zip_path = os.path.join(dist_dir, zip_name)
    
    # Check for existing package
    if not check_existing_package(zip_path, zip_name):
        return False
    
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("root.py", create_standalone_root_py())
            zf.writestr("requirements.txt", create_root_requirements())
            zf.writestr("setup.bat", create_root_setup_bat())
            zf.writestr("setup.sh", create_root_setup_sh())
            zf.writestr("README.txt", """Party Pool Root/Admin
=====================

Setup Instructions:
-------------------
Windows: Run setup.bat, then run 'python root.py'
Linux/Mac: Run 'chmod +x setup.sh && ./setup.sh', then run 'python3 root.py'

Usage:
------
1. Run the root client (python root.py)
2. Enter the root password provided by the server administrator
3. Type 'list' to see available commands
4. Use commands to manage the server

Available Commands:
-------------------
list                              - Show all commands
close-server [-t <sec>] [-m "msg"] - Shutdown server
list-conn [-ip | -u]              - List connections
remove [-ip <ip> | -u <user>]     - Kick user
send [-all | -ip <ips>] "msg"     - Broadcast message
exit                              - Logout

Press Ctrl+C to exit.
""")
        
        print_success(f"Root ZIP created: {os.path.abspath(zip_path)}")
        return True
        
    except Exception as e:
        print_error(f"Failed to generate root ZIP: {e}")
        cleanup_failed_dist(dist_dir, "root")
        return False


def reset_ip_validation():
    """Reset the IP validation flag (call at start of new distribution session)."""
    global _encrypted_ip_validated
    _encrypted_ip_validated = False


def handle_distribution():
    """Handle distribution package generation."""
    # Reset IP validation at start of each distribution session
    reset_ip_validation()
    
    while True:
        display_distribution_menu()
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == "1":
            display_choose_os()
            os_choice = input("Enter your choice (1-4): ").strip()
            
            if os_choice == "1":
                print_info("Generating client package for Windows...")
                if generate_client_package():
                    print_info(f"Distribution files are in: {os.path.abspath('dist')}")
                input("\nPress Enter to continue...")
                reset_ip_validation()
            elif os_choice == "2":
                print_info("Generating client zip for Linux/macOS...")
                if generate_client_zip():
                    print_info(f"Distribution files are in: {os.path.abspath('dist')}")
                input("\nPress Enter to continue...")
                reset_ip_validation()
            elif os_choice == "3":
                print_info("Generating client packages for both OSes...")
                success = generate_client_package()
                if success:
                    success = generate_client_zip(skip_ip_check=True)
                if success:
                    print_info(f"Distribution files are in: {os.path.abspath('dist')}")
                input("\nPress Enter to continue...")
                reset_ip_validation()
            elif os_choice == "4":
                reset_ip_validation()
                continue
            else:
                print_error("Invalid choice. Please enter 1-4.")
                input("Press Enter to continue...")
                reset_ip_validation()
                continue
            
        elif choice == "2":
            display_choose_os()
            os_choice = input("Enter your choice (1-4): ").strip()
            
            if os_choice == "1":
                print_info("Generating root package for Windows...")
                if generate_root_package():
                    print_info(f"Distribution files are in: {os.path.abspath('dist')}")
                input("\nPress Enter to continue...")
                reset_ip_validation()
            elif os_choice == "2":
                print_info("Generating root zip for Linux/macOS...")
                if generate_root_zip():
                    print_info(f"Distribution files are in: {os.path.abspath('dist')}")
                input("\nPress Enter to continue...")
                reset_ip_validation()
            elif os_choice == "3":
                print_info("Generating root packages for both OSes...")
                success = generate_root_package()
                if success:
                    success = generate_root_zip(skip_ip_check=True)
                if success:
                    print_info(f"Distribution files are in: {os.path.abspath('dist')}")
                input("\nPress Enter to continue...")
                reset_ip_validation()
            elif os_choice == "4":
                reset_ip_validation()
                continue
            else:
                print_error("Invalid choice. Please enter 1-4.")
                input("Press Enter to continue...")
                reset_ip_validation()
                continue
            
        elif choice == "3":
            display_choose_os()
            os_choice = input("Enter your choice (1-4): ").strip()
            
            if os_choice == "1":
                print_info("Generating client and root packages for Windows...")
                success = generate_client_package()
                if success:
                    success = generate_root_package(skip_ip_check=True)
                if success:
                    print_info(f"Distribution files are in: {os.path.abspath('dist')}")
                input("\nPress Enter to continue...")
                reset_ip_validation()
            elif os_choice == "2":
                print_info("Generating client and root zips for Linux/macOS...")
                success = generate_client_zip()
                if success:
                    success = generate_root_zip(skip_ip_check=True)
                if success:
                    print_info(f"Distribution files are in: {os.path.abspath('dist')}")
                input("\nPress Enter to continue...")
                reset_ip_validation()
            elif os_choice == "3":
                print_info("Generating client and root packages for both OSes...")
                success = generate_client_package()
                if success:
                    success = generate_client_zip(skip_ip_check=True)
                if success:
                    success = generate_root_package(skip_ip_check=True)
                if success:
                    success = generate_root_zip(skip_ip_check=True)
                if success:
                    print_info(f"Distribution files are in: {os.path.abspath('dist')}")
                input("\nPress Enter to continue...")
                reset_ip_validation()
            elif os_choice == "4":
                reset_ip_validation()
                continue
            else:
                print_error("Invalid choice. Please enter 1-4.")
                input("Press Enter to continue...")
                reset_ip_validation()
                continue
            
        elif choice == "4":
            print_info("Returning to main menu...")
            reset_ip_validation()
            clear_screen()
            return
            
        else:
            print_error("Invalid choice. Please enter 1-4.")
            input("Press Enter to continue...")
            reset_ip_validation()


def party_pool():
    """Main application loop."""
    while True:
        display_menu()
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == "1":
            print_info("Starting server...")
            try:
                if ensure_encrypted_ip():
                    from server.server import start_server
                    start_server()
                else:
                    print_error("Server startup aborted due to encrypted IP issues.")
                    input("Press Enter to continue...")
            except KeyboardInterrupt:
                print_error("\nServer stopped by user.")
                input("Press Enter to continue...")
            except Exception as e:
                print_error(f"Error starting server: {e}")
                input("Press Enter to continue...")
        
        elif choice == "2":
            handle_distribution()
        
        elif choice == "3":
            print_info("Starting root login...")
            try:
                from root.root import init_root
                init_root()
            except KeyboardInterrupt:
                print_error("\nRoot session ended.")
                input("Press Enter to continue...")
            except Exception as e:
                print_error(f"Error in root login: {e}")
                input("Press Enter to continue...")
        
        elif choice == "4":
            print_info("Starting client login...")
            try:
                from client.client import start_client
                start_client()
            except KeyboardInterrupt:
                print_error("\nClient session ended.")
                input("Press Enter to continue...")
            except Exception as e:
                print_error(f"Error in client login: {e}")
                input("Press Enter to continue...")
        
        elif choice == "5":
            clear_screen()
            print_success("Goodbye!")
            time.sleep(1)
            sys.exit(0)
        
        else:
            print_error("Invalid choice. Please enter 1-5.")
            input("Press Enter to continue...")
            clear_screen()


if __name__ == "__main__":
    try:
        party_pool()
    except KeyboardInterrupt:
        print_error("\n\nApplication interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print_error(f"Fatal error: {e}")
        sys.exit(1)
