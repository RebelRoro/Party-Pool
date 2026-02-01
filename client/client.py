"""
Party Pool Client - Chat client for connecting to Party Pool Server.
"""

import socket
import threading
import asyncio
import getpass
import time
import sys
import os
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
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

client_socket = None
u_name = None
ENCRYPTED_IP = None
client_ip = None


def display_banner():
    """Display Party Pool banner."""
    clear_screen()
    intro_text = "Connecting to Party Pool..."
    slow_type(intro_text, delay=0.06)
    time.sleep(0.5)
    clear_screen()
    
    banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║            🎉 PARTY POOL - Chat Server 🎉                 ║
║                                                           ║
║           Where messages flow and fun begins!             ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

💬 Connected and Ready!
📝 Type /help for available commands
📝 Press Ctrl+D/Ctrl+C to exit
    """
    print(banner)


def display_help():
    """Display available client commands."""
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
    """Display online users in a formatted box."""
    # Parse: ONLINE_USERS:color1:user1|color2:user2|...
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
            # Pad username to fit box
            padded = username.center(40)
            print_formatted_text(HTML(f'<b>║ <{color}>{padded}</{color}> ║</b>'))
    
    print_formatted_text(HTML('<b>╚══════════════════════════════════════════╝</b>'))


def receive_messages(client_socket):
    """Receive and display messages from server."""
    while True:
        try:
            message = client_socket.recv(config.BUFFER_SIZE).decode('utf-8')
            if message:
                if message.startswith("ONLINE_USERS:"):
                    display_online_users(message)
                elif message.startswith("YOUR_IP:"):
                    ip = message.replace("YOUR_IP:", "")
                    print_formatted_text(HTML(f'<b><ansicyan>Your IP address: </ansicyan><ansigreen>{ip}</ansigreen></b>'))
                elif message.startswith("REQUEST_OK"):
                    print_formatted_text(HTML('<b><ansigreen>✓ Your request has been submitted to the server admin.</ansigreen></b>'))
                elif message.startswith("REQUEST_FAIL"):
                    print_formatted_text(HTML('<b><ansired>✗ Failed to submit request. Please try again.</ansired></b>'))
                elif "------------------------WELCOME" in message:
                    print_formatted_text(HTML(f'<b><ansigreen>{message}</ansigreen></b>'))
                elif "------------------------GOOD BYE" in message:
                    print_formatted_text(HTML(f'<b><ansired>{message}</ansired></b>'))
                elif "$root@party-pool:" in message:
                    print_formatted_text(HTML(f"<b><ansired>{message}</ansired></b>"))
                else:
                    print_formatted_text(HTML(f'<b><ansicyan>{message}</ansicyan></b>'))
        except Exception as e:
            print_error("Connection lost. Exiting...")
            sys.stdout.flush()
            time.sleep(5)
            clear_screen()
            os._exit(0)


def handle_client_command(message):
    """Handle client-side commands. Returns True if command was handled locally."""
    cmd = message.strip().lower()
    
    if cmd == '/help':
        display_help()
        return True
    elif cmd == '/exit':
        print_warning("Disconnecting from Party Pool...")
        sys.stdout.flush()
        time.sleep(2)
        clear_screen()
        os._exit(0)
    
    # These commands are sent to server
    return False

def validate_message(message):
    """Validate message before sending."""
    if not message.strip():
        print_error("Cannot send empty message.")
        return False
    if any(char in message for char in config.ILLEGAL_CHARS):
        print_error(f"Message contains illegal characters: [{', '.join(config.ILLEGAL_CHARS)}]")
        return False
    return True

async def send_messages_loop(session, client_socket):
    """Send messages to server."""
    global u_name
    
    print_info(f'Connected as: {u_name}')
    
    while True:
        try:
            message = await session.prompt_async(f"${u_name}: ")
            
            if validate_message(message):
                # Handle local commands first
                if handle_client_command(message):
                    continue
                
                # Send to server
                client_socket.send(message.encode('utf-8'))
                
        except EOFError:
            print_error('Exiting...')
            sys.stdout.flush()
            time.sleep(2)
            clear_screen()
            os._exit(0)
        except KeyboardInterrupt:
            print_error('Interrupted. Exiting...')
            sys.stdout.flush()
            time.sleep(2)
            clear_screen()
            os._exit(0)
        except Exception as e:
            print_error(f'Error: {e}')
            sys.stdout.flush()
            time.sleep(5)
            clear_screen()
            os._exit(0)


def start_client():
    """Start the Party Pool client."""
    global client_socket, u_name, ENCRYPTED_IP, client_ip
    
    print_info("Enter passkey to connect to server: ")
    passwd = getpass.getpass("").strip()
    
    try:
        if not ENCRYPTED_IP:
            try:
                with open(config.ENCRYPTED_IP_FILE, 'r', encoding='utf-8') as f:
                    ENCRYPTED_IP = f.read().strip()
            except FileNotFoundError:
                print_error(f"Encrypted IP file not found: {config.ENCRYPTED_IP_FILE}")
                time.sleep(5)
                return
        
        server_ip = decrypt_ip(ENCRYPTED_IP, passwd)
    except Exception as e:
        print_error("Connection failed: Wrong passkey or corrupted IP address.")
        logger.error(f"Decryption error: {e}")
        sys.stdout.flush()
        time.sleep(5)
        return
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect((server_ip, config.SERVER_PORT))
        
        # Get client's own IP
        client_ip = client_socket.getsockname()[0]
        
        # Send authentication
        auth_token = compute_hmac(passwd, config.AUTH_MESSAGE)
        client_socket.send(len(auth_token).to_bytes(2, "big") + auth_token)
        
        # Check for duplicate IP
        duplicate_client = client_socket.recv(64)
        if duplicate_client == b'YES-IP':
            print_error("A session already exists from this machine. Close any previous sessions and try again.")
            sys.stdout.flush()
            time.sleep(5)
            client_socket.close()
            return
        
        # Wait for server response
        try:
            reply = client_socket.recv(64)
        except Exception:
            print_error("No reply from server.")
            sys.stdout.flush()
            time.sleep(5)
            client_socket.close()
            return
        
        if reply == b"OK":
            print_success("Authenticated successfully!")
            time.sleep(2)
            display_banner()
            
            # Get username with loop on invalid/duplicate
            while True:
                print_info("Enter your username (no spaces, not 'root'): ")
                u_name = input().strip().replace(" ", "")
                
                if not u_name:
                    print_error("Username cannot be empty. Try again.")
                    continue
                    
                client_socket.send(u_name.encode('utf-8'))
                
                # Check for duplicate/invalid username
                username_response = client_socket.recv(64)
                if username_response == b'YES-U':
                    print_error("Username already exists or is invalid. Try another username.")
                    continue
                else:
                    # Username accepted
                    break
            
            # Start receiver thread
            thread_receive = threading.Thread(
                target=receive_messages,
                args=(client_socket,),
                daemon=True
            )
            thread_receive.start()
            
            # Send messages
            with patch_stdout():
                session = PromptSession()
                asyncio.run(send_messages_loop(session, client_socket))
        
        else:
            print_error("Authentication failed. Ensure you have the correct passkey.")
            time.sleep(5)
            client_socket.close()
            return
    
    except Exception as e:
        print_error(f'Connection Error: {e}')
        logger.error(f"Connection error: {e}")
        sys.stdout.flush()
        time.sleep(5)
    
    finally:
        if client_socket:
            client_socket.close()


if __name__ == "__main__":
    start_client()
