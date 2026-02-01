"""
Party Pool Root - Administrative control interface for server management.
"""

import socket
import asyncio
import getpass
import time
import sys
import os
import threading
import pickle as pkl
from prompt_toolkit.shortcuts import print_formatted_text
from prompt_toolkit.formatted_text import HTML

import config
from util import (
    setup_logger,
    compute_hmac,
    decrypt_ip,
    clear_screen,
    slow_type,
    print_success,
    print_error,
    print_info,
    print_warning,
)

logger = setup_logger(__name__, config.SERVER_LOG)

root_socket = None
ENCRYPTED_IP = None


def display_banner():
    """Display root login banner."""
    clear_screen()
    intro_text = "Logging in as root..."
    slow_type(intro_text, delay=0.08)
    time.sleep(2)
    clear_screen()
    
    banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║        ⚙️  PARTY POOL - ROOT CONTROL PANEL ⚙️             ║
║                                                           ║
║            Administrative Control Interface               ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

🔑 Logged in as root with full privileges
📋 Type 'list' for available commands
⚠️ Press Ctrl+C to exit
    """
    print(banner)


def display_list():
    """Display available root commands (local)."""
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
    """Receive messages from server."""
    while True:
        try:
            message = pkl.loads(root_socket.recv(2048))
            if message:
                print(message)
            else:
                continue
        except Exception as e:
            continue


def handle_local_command(cmd):
    """Handle commands that run locally without server interaction.
    Returns True if command was handled locally, False otherwise.
    """
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
    """Send commands to server."""
    global root_socket
    
    while True:
        try:
            print_formatted_text(HTML(f"<ansired>$root@party-pool:</ansired> "), end="")
            
            cmd = await asyncio.to_thread(input)
            
            if not cmd or not cmd.strip():
                continue
            
            # Handle local commands first
            if handle_local_command(cmd):
                continue
            
            # Send to server
            if root_socket:
                root_socket.send(cmd.encode('utf-8'))
                cmd_exe = root_socket.recv(64)
            else:
                print_error("Not connected to server.")
                continue
            
            if cmd_exe == b'OK':
                print_success("\nCommand executed successfully.\n")
            elif cmd_exe == b'FAIL':
                print_error("Command failed.\n")
            else:
                continue
        except pkl.UnpicklingError:
            continue
        except KeyboardInterrupt:
            print_error('\nInterrupted. Exiting...')
            sys.stdout.flush()
            time.sleep(2)
            clear_screen()
            os._exit(0)
        except Exception as e:
            print_error("\nServer connection lost.")
            logger.error(f"Error in send_command: {e}")
            sys.stdout.flush()
            time.sleep(2)
            clear_screen()
            os._exit(0)


def handle_root():
    """Handle root connection session."""
    global root_socket
    
    try:
        # Start receiver thread
        thread_receive = threading.Thread(
            target=receive_messages,
            args=(root_socket,),
            daemon=True
        )
        thread_receive.start()
        
        # Send commands
        asyncio.run(send_command())
        
    except Exception as e:
        print_error(f"\nError: {e}")
        logger.error(f"Error in handle_root: {e}")
        return


def init_root():
    """Initialize root login and control."""
    global root_socket, ENCRYPTED_IP
    
    print_info("Enter the server passkey (same as client passkey): ")
    passkey = getpass.getpass("").strip()
    
    print_info("Enter root password: ")
    root_passwd = getpass.getpass("").strip()
    
    try:
        if not ENCRYPTED_IP:
            try:
                with open(config.ENCRYPTED_IP_FILE, 'r', encoding='utf-8') as f:
                    ENCRYPTED_IP = f.read().strip()
            except FileNotFoundError:
                print_error(f"Encrypted IP file not found: {config.ENCRYPTED_IP_FILE}")
                time.sleep(5)
                return
        
        # Decrypt IP using passkey (same as client uses)
        server_ip = decrypt_ip(ENCRYPTED_IP, passkey)
    except Exception as e:
        print_error("Connection failed: Wrong passkey or corrupted IP address.")
        logger.error(f"Decryption error: {e}")
        sys.stdout.flush()
        time.sleep(5)
        return
    
    root_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        root_socket.connect((server_ip, config.SERVER_PORT))
        
        # Send root authentication using root password
        auth_token = compute_hmac(root_passwd, config.ROOT_AUTH)
        root_socket.send(len(auth_token).to_bytes(2, "big") + auth_token)
        
        # Wait for response
        try:
            reply = root_socket.recv(64)
        except Exception:
            print_error("No reply from server.")
            sys.stdout.flush()
            time.sleep(5)
            root_socket.close()
            return
        
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
        print_error(f'Connection Error: {e}')
        logger.error(f"Connection error: {e}")
        sys.stdout.flush()
        time.sleep(5)
    
    finally:
        if root_socket:
            root_socket.close()


if __name__ == "__main__":
    init_root()
