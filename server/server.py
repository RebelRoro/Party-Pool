"""
Party Pool Server - Main server handler.
Manages client and root connections.
"""

import time
import socket
import threading
import os
import hmac
import pickle as pkl
import ipaddress as ipa

import config
from util import setup_logger, compute_hmac, clear_screen
from util.common import print_error

logger = setup_logger(__name__, config.SERVER_LOG)


class ServerManager:
    """Manages server operations and client connections."""
    
    def __init__(self):
        self.clients = []
        self.clients_uname = {}
        self.clients_sockets = {}
        self.root = []
        self.server = None
        
        # Root command handlers
        self.COMMANDS = {
            "list": self.cmd_list_help,
            "close-server": self.cmd_close_server,
            "list-conn": self.cmd_list_conn,
            "remove": self.cmd_remove_conn,
            "send": self.cmd_send_msg,
            "exit": self.cmd_exit_root,
        }
    
    # ==================== ROOT COMMAND HANDLERS ====================
    
    def cmd_list_help(self, args):
        """List all available root commands."""
        if args:
            return "Invalid syntax. Use 'list' without arguments."
        
        help_message = (
            "\n|--------------Command--------------|------------------------------------Description------------------------------------|\n"
            "| list                              | Lists all available commands                                                      |\n"
            "| close-server [-t <t>] [-m \"msg\"]  | Closes the server [after time t seconds] [with reason message]                    |\n"
            "| list-conn [-ip | -u]              | Lists active connections [only IP addresses | only usernames]                     |\n"
            "| remove [-ip <ip> | -u <u>]        | Removes the provided IP address or username from active connections               |\n"
            "| send [-all | -ip <ip(s)>] [\"msg\"] | Broadcasts message to all clients or to the given IP addresses separated by spaces|\n"
            "| exit                              | Logout from root                                                                  |\n"
            "|-----------------------------------|-----------------------------------------------------------------------------------|\n"
        )
        return self.root_broadcast(help_message, mode="to-root")
    
    def cmd_close_server(self, args):
        """Close the server with optional delay and message."""
        delay = 0
        message = "Server has shut down..."
        
        if args:
            try:
                i = 0
                while i < len(args):
                    if args[i] == '-t' and i + 1 < len(args):
                        delay = int(args[i + 1])
                        i += 2
                    elif args[i] == '-m' and i + 1 < len(args):
                        # Get message (everything after -m as string, handling quotes)
                        msg_parts = args[i + 1:]
                        message = " ".join(msg_parts).strip('"')
                        break
                    else:
                        return "Invalid syntax. Use 'list' to see command formats."
            except (ValueError, IndexError) as e:
                return f"Invalid syntax: {e}"
        
        if delay > 0:
            self.root_broadcast(f"Server shutting down in {delay} seconds: {message}", mode="all")
            logger.warning(f"Server shutdown initiated by root in {delay}s: {message}")
            time.sleep(delay)
        
        logger.warning(f"Server shutdown by root: {message}")
        self.root_broadcast(message)
        time.sleep(1)
        clear_screen()
        os._exit(0)
    
    def cmd_list_conn(self, args):
        """List active connections."""
        try:
            if not args:
                message = f"Active Connections: {self.clients_uname}"
            elif args[0] == '-ip' and len(args) == 1:
                message = f"Connected IPs: {list(self.clients_uname.keys())}"
            elif args[0] == '-u' and len(args) == 1:
                message = f"Connected Users: {list(self.clients_uname.values())}"
            else:
                return "Invalid syntax. Use 'list' to see command formats."
        except Exception as e:
            return f"Error: {e}"
        
        return self.root_broadcast(message, mode="to-root")
    
    def cmd_remove_conn(self, args):
        """Remove a client by IP or username."""
        try:
            if len(args) < 2:
                return "Invalid syntax. Use 'remove -ip <ip>' or 'remove -u <username>'."
            
            if args[0] == '-ip':
                ip = args[1]
                if not self._validate_ip(ip):
                    return f"Invalid IP address: {ip}"
                if self.root and ip == self.get_ip_from_uname('root'):
                    return "Cannot remove root connection using this command. Use 'exit' instead."
                if ip not in self.clients_uname.keys():
                    return f"IP '{ip}' not found in active connections."
                
                username = self.clients_uname.get(ip)
                logger.warning(f"Root removed '{ip}':'{username}' from active users")
                self.root_broadcast("You have been removed from the server by admin.", mode="", clients_to_send=[self.clients_sockets.get(ip)])
                self.remove_client(self.clients_sockets.get(ip), (ip, username))
                self.refresh_clients()
                return self.root_broadcast(f"'{ip}':'{username}' removed from active connections.", mode="to-root")
            
            elif args[0] == '-u':
                username = args[1]
                if username.lower() == 'root':
                    return "Cannot remove root. Use 'exit' to logout."
                if username not in self.clients_uname.values():
                    return f"Username '{username}' not found in active connections."
                
                ip = self.get_ip_from_uname(username)
                logger.warning(f"Root removed '{ip}':'{username}' from active users")
                self.root_broadcast("You have been removed from the server by admin.", mode="", clients_to_send=[self.clients_sockets.get(ip)])
                self.remove_client(self.clients_sockets.get(ip), (ip, username))
                self.refresh_clients()
                return self.root_broadcast(f"'{ip}':'{username}' removed from active connections.", mode="to-root")
            
            else:
                return "Invalid syntax. Use 'remove -ip <ip>' or 'remove -u <username>'."
        
        except Exception as e:
            return f"Error: {e}"
    
    def cmd_send_msg(self, args):
        """Send message to clients."""
        try:
            if len(args) < 2:
                return "Invalid syntax. Use 'send -all \"message\"' or 'send -ip <ip1> <ip2> \"message\"'."
            
            if args[0] == '-all':
                message = " ".join(args[1:]).strip('"')
                return self.root_broadcast(message)
            
            elif args[0] == '-ip':
                # Parse: -ip ip1 ip2 ip3 "message"
                raw = " ".join(args[1:])
                if '"' not in raw:
                    return "Message must be enclosed in quotes."
                
                parts = raw.split('"')
                ip_part = parts[0].strip()
                message = parts[1] if len(parts) > 1 else ""
                
                ips = ip_part.split()
                sock_list = []
                
                for ip in ips:
                    if not self._validate_ip(ip):
                        return f"Invalid IP address: {ip}"
                    if ip in self.clients_sockets:
                        sock_list.append(self.clients_sockets[ip])
                    else:
                        return f"IP '{ip}' not connected."
                
                if not sock_list:
                    return "No valid recipients found."
                
                result = self.root_broadcast(message, mode="", clients_to_send=sock_list)
                self.root_broadcast(f"Message sent to {len(sock_list)} client(s).", mode="to-root")
                return result
            
            else:
                return "Invalid syntax. Use 'send -all \"message\"' or 'send -ip <ips> \"message\"'."
        
        except IndexError:
            return "Invalid IP addresses or message format."
        except Exception as e:
            return f"Error: {e}"
    
    def cmd_exit_root(self, args):
        """Exit root session."""
        if args:
            return "Invalid syntax. Use 'exit' without arguments."
        return b'EXIT'
    
    def cmd_run(self, cmd, args):
        """Execute a root command."""
        if cmd in self.COMMANDS:
            return self.COMMANDS[cmd](args)
        else:
            return "Invalid command. Use 'list' to see available commands."
    
    def _validate_ip(self, ip):
        """Validate IP address format."""
        try:
            ipa.IPv4Address(ip)
            return True
        except ipa.AddressValueError:
            return False
    
    # ==================== CONNECTION MANAGEMENT ====================
    
    def refresh_clients(self):
        """Refresh server display with current connections."""
        clear_screen()
        print(f"Server is listening on {config.SERVER_HOST}:{config.SERVER_PORT}...")
        print("Current Connections:")
        if self.root:
            print(f"Root Connection - {self.root[0]}")
        for key, value in self.clients_uname.items():
            try:
                print(f"Connection with {key} - {value}")
            except Exception as e:
                logger.warning(f"Conflict getting client details | {e}")
                continue
    
    def remove_client(self, client_socket, client_address, send_exit_message=True):
        """Remove client from active connections."""
        try:
            temp = self.clients_uname.get(client_address[0], "")
            if send_exit_message and temp:
                self.exit_message(temp, client_socket, client_address)
            
            if self.clients_uname.get(client_address[0]):
                del self.clients_uname[client_address[0]]
            if self.clients_sockets.get(client_address[0]):
                del self.clients_sockets[client_address[0]]
            
            logger.warning(f"Connection lost from {client_address[0]} - {temp}")
            client_socket.close()
            self.refresh_clients()
            
            try:
                self.clients.remove(client_socket)
            except Exception as e:
                logger.warning(f"Client socket not in clients list | {e}")
        except Exception as e:
            logger.warning(f"Conflict removing client | {e}")
            return e
    
    def get_ip_from_sock(self, sock):
        """Get IP address from socket."""
        if self.root and sock == self.root[1]:
            return self.root[0]
        for key, value in self.clients_sockets.items():
            if value == sock:
                return key
        return None
    
    def get_ip_from_uname(self, u_name):
        """Get IP address from username."""
        if u_name == 'root':
            return self.root[0] if self.root else None
        for key, value in self.clients_uname.items():
            if value == u_name:
                return key
        return None
    
    def entry_message(self, u_name, client_socket, client_address):
        """Send welcome message to all clients."""
        for client in self.clients:
            if client != client_socket:
                try:
                    client.sendall(f"------------------------WELCOME {u_name}------------------------".encode('utf-8'))
                except:
                    self.remove_client(client, client_address)
                    self.refresh_clients()
                    continue
        logger.info(f"Welcome message sent for {client_address[0]} - {u_name}")
    
    def exit_message(self, u_name, client_socket, client_address):
        """Send goodbye message to all clients."""
        for client in self.clients:
            if client != client_socket:
                try:
                    client.sendall(f"------------------------GOOD BYE {u_name}------------------------".encode('utf-8'))
                except:
                    self.remove_client(client, client_address)
                    self.refresh_clients()
                    continue
        logger.info(f"Good bye message sent for {client_address[0]} - {u_name}")
    
    def broadcast_message(self, message, client_socket, client_address):
        """Broadcast message to all clients or handle client commands."""
        msg_stripped = message.strip()
        msg_lower = msg_stripped.lower()
        
        logger.debug(f"Processing message: '{msg_stripped}' (lower: '{msg_lower}')")
        
        # Handle client commands
        if msg_lower == '/online':
            logger.info(f"Command /online from {client_address[0]}")
            self.send_online_users(client_socket)
            return
        elif msg_lower == '/ip':
            logger.info(f"Command /ip from {client_address[0]}")
            self.send_client_ip(client_socket, client_address)
            return
        elif msg_lower.startswith('/request '):
            request_msg = msg_stripped[9:]  # Remove '/request '
            logger.info(f"Command /request from {client_address[0]}: {request_msg}")
            self.handle_client_request(client_socket, client_address, request_msg)
            return
        elif msg_lower == '/request':
            client_socket.send("REQUEST_FAIL:Empty request message".encode('utf-8'))
            return
        
        # Regular message broadcast
        for client in self.clients:
            if client != client_socket:
                try:
                    client.send(f"${self.clients_uname[client_address[0]]}\n    |==> {message}".encode('utf-8'))
                except:
                    self.remove_client(client_socket, client_address)
                    self.refresh_clients()
                    continue
    
    def send_client_ip(self, client_socket, client_address):
        """Send client's IP address back to them."""
        try:
            client_socket.send(f"YOUR_IP:{client_address[0]}".encode('utf-8'))
        except Exception as e:
            logger.warning(f"Error sending IP to client: {e}")
    
    def handle_client_request(self, client_socket, client_address, request_msg):
        """Handle client request and save to file."""
        try:
            username = self.clients_uname.get(client_address[0], "Unknown")
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            
            with open("client_requests.txt", "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] {username} ({client_address[0]}): {request_msg}\n")
            
            client_socket.send("REQUEST_OK".encode('utf-8'))
            logger.info(f"Request saved from {username}: {request_msg}")
        except Exception as e:
            client_socket.send("REQUEST_FAIL".encode('utf-8'))
            logger.error(f"Error saving request: {e}")
    
    def send_online_users(self, requesting_socket):
        """Send list of online users to requesting client."""
        import random
        colors = ['ansigreen', 'ansiyellow', 'ansiblue', 'ansimagenta', 'ansicyan', 'ansiwhite']
        
        users = list(self.clients_uname.values())
        if not users:
            requesting_socket.send("ONLINE_USERS:No users online".encode('utf-8'))
            return
        
        # Create colored user list
        user_list = []
        for user in users:
            color = random.choice(colors)
            user_list.append(f"{color}:{user}")
        
        message = "ONLINE_USERS:" + "|".join(user_list)
        requesting_socket.send(message.encode('utf-8'))
    
    def root_broadcast(self, message, mode="all", clients_to_send=[]):
        """Broadcast message from root to clients."""
        if mode == "to-root":
            if message:
                try:
                    if self.root:
                        self.root[1].sendall(pkl.dumps(message))
                    return True
                except Exception as e:
                    return f"Error while sending message to root | {e}"
            return True
        
        if mode == "all":
            clients_to_send = self.clients.copy()
        
        if not clients_to_send:
            return "No clients selected to broadcast message."
        
        for client in clients_to_send:
            try:
                ip = self.get_ip_from_sock(client)
                if self.clients_uname.get(ip) != "root":
                    try:
                        client.sendall(f"\n\n$root@party-pool: {message}\n\n".encode('utf-8'))
                        logger.info(f"Message sent to client '{ip}':'{self.clients_uname.get(ip)}' by root")
                    except Exception as e:
                        logger.warning(f"Error while sending message to client | {e}")
                        self.remove_client(client, (ip, self.clients_uname.get(ip)))
                        self.refresh_clients()
                        continue
            except Exception as e:
                logger.warning(f"Error while broadcasting | {e}")
                continue
        
        if mode == "all":
            self.root_broadcast("Message sent to client(s).", mode="to-root")
        return True
    
    def check_duplicate_client(self, value):
        """Check if client/username already exists."""
        return (value in self.clients_uname.keys() or 
                value in self.clients_uname.values() or 
                value in self.clients_sockets.keys() or 
                value.lower() in ["root", ""])
    
    def handle_client(self, client_socket, client_address):
        """Handle individual client connections."""
        self.entry_message(self.clients_uname.get(client_address[0]), client_socket, client_address)
        
        while True:
            try:
                if client_address[0] not in self.clients_uname.keys():
                    client_socket.send("Your connection has been disrupted. Please reconnect.".encode('utf-8'))
                    client_socket.close()
                    self.remove_client(client_socket, client_address)
                    self.refresh_clients()
                    return
            except Exception as e:
                logger.warning(f"Client socket error | {e}")
            
            try:
                message = client_socket.recv(config.BUFFER_SIZE).decode('utf-8')
                if message:
                    self.broadcast_message(message, client_socket, client_address)
                    logger.info(f"Message Broadcast: IP='{client_address[0]}' | User='{self.clients_uname.get(client_address[0])}' | Msg='{message}'")
            except ValueError as e:
                break
            except Exception as e:
                logger.error(f"Error while sending message | {e}")
                self.remove_client(client_socket, client_address)
                self.refresh_clients()
                break
    
    def init_client_conn(self, client_socket, client_address):
        """Initialize new client connection."""
        try:
            self.clients.append(client_socket)
            self.clients_sockets[client_address[0]] = client_socket
            
            # Username loop - keep asking until valid username received
            while True:
                u_name = client_socket.recv(config.BUFFER_SIZE).decode('utf-8')
                
                if self.check_duplicate_client(u_name):
                    client_socket.send(b'YES-U')
                    logger.warning(f"Illegal username '{u_name}' from '{client_address[0]}'")
                    continue
                else:
                    client_socket.send(b'$')
                    break
            
            self.clients_uname[client_address[0]] = u_name
            self.refresh_clients()
            logger.info(f"Connection with {client_address[0]} - {u_name}")
            
            server_thread = threading.Thread(
                target=self.handle_client, 
                args=(client_socket, client_address,)
            )
            server_thread.daemon = True
            server_thread.start()
        except Exception as e:
            logger.warning(f"Connection reset from {client_address[0]} | {e}")
            self.remove_client(client_socket, client_address, send_exit_message=False)
            self.refresh_clients()
    
    def root_conn(self, client_socket, client_address):
        """Handle root connection and process commands."""
        self.root = [client_address[0], client_socket]
        self.refresh_clients()
        logger.info(f"ROOT LOGIN FROM '{client_address[0]}'")
        
        while True:
            try:
                command = client_socket.recv(config.BUFFER_SIZE).decode('utf-8').strip()
                if not command:
                    continue
                
                parts = command.split()
                cmd = parts[0].lower()
                args = parts[1:] if len(parts) > 1 else []
                
                try:
                    result = self.cmd_run(cmd, args)
                    
                    if result == b'EXIT':
                        logger.info(f"ROOT LOGOUT FROM '{client_address[0]}'")
                        client_socket.send(b'EXIT')
                        break
                    elif isinstance(result, str):
                        # Error message - send to root
                        self.root_broadcast(result, mode="to-root")
                        client_socket.send(b'FAIL')
                    elif result is True:
                        client_socket.send(b'OK')
                    else:
                        client_socket.send(b'OK')
                        
                except Exception as e:
                    logger.error(f"Command execution error: {e}")
                    self.root_broadcast(f"Error: {e}", mode="to-root")
                    client_socket.send(b'FAIL')
                    
            except Exception as e:
                logger.error(f"ROOT CONNECTION LOST - {client_address[0]} | {e}")
                break
        
        # Cleanup root connection
        if self.root:
            self.root.clear()
        self.refresh_clients()
    
    def start(self):
        """Start the server."""
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((config.SERVER_HOST, config.SERVER_PORT))
            self.server.listen()
            # self.server.listen(config.MAX_CONNECTIONS)
            self.refresh_clients()
            logger.info(f"Server listening on {config.SERVER_HOST}:{config.SERVER_PORT}")
        except Exception as e:
            logger.error(f"Error starting server | {e}")
            print_error(f"Error starting server | {e}")
            input("Press Enter to continue...")
            return
        
        while True:
            try:
                client_socket, client_address = self.server.accept()
                
                try:
                    header = client_socket.recv(2)
                    if len(header) < 2:
                        logger.error(f"Error reading auth token from {client_address[0]}")
                        client_socket.close()
                        continue
                    
                    token_len = int.from_bytes(header, "big")
                    token = client_socket.recv(token_len)
                    if len(token) != token_len:
                        logger.error(f"Token mismatch from {client_address[0]}")
                        client_socket.close()
                        continue
                except Exception as e:
                    logger.error(f"Error reading auth token from {client_address[0]} | {e}")
                    client_socket.close()
                    continue
                
                # Check for root connection
                root_hmac = compute_hmac(config.ROOT_PASSWORD, config.ROOT_AUTH)
                if hmac.compare_digest(root_hmac, token) and not self.root:
                    logger.info(f"INITIATED ROOT LOGIN FROM '{client_address[0]}'")
                    client_socket.send(b'ROOT-OK')
                    root_thread = threading.Thread(
                        target=self.root_conn,
                        args=(client_socket, client_address,),
                        daemon=True
                    )
                    root_thread.start()
                    continue
                
                # Check for duplicate IP
                if self.check_duplicate_client(client_address[0]):
                    client_socket.send(b'YES-IP')
                    logger.warning(f"Duplicate session blocked from '{client_address[0]}'")
                    self.remove_client(client_socket, client_address, send_exit_message=False)
                    self.refresh_clients()
                    continue
                else:
                    client_socket.send(b'$')
                
                # Check client authentication
                expected_hmac = compute_hmac(config.CLIENT_PASSKEY, config.AUTH_MESSAGE)
                if hmac.compare_digest(expected_hmac, token):
                    logger.info(f"Client authenticated with {client_address[0]}")
                    client_socket.send(b"OK")
                    client_thread = threading.Thread(
                        target=self.init_client_conn,
                        args=(client_socket, client_address,),
                        daemon=True
                    )
                    client_thread.start()
                    continue
                else:
                    logger.warning(f"Authentication failed from {client_address[0]}")
                    client_socket.send(b"FAIL")
                    client_socket.close()
                    self.remove_client(client_socket, client_address, send_exit_message=False)
                    self.refresh_clients()
                    continue
            
            except Exception as e:
                logger.error(f"Error accepting connection | {e}")
                continue


def start_server():
    """Start the Party Pool server."""
    manager = ServerManager()
    manager.start()


if __name__ == "__main__":
    start_server()
