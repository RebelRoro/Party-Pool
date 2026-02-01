"""
Shared utilities for Party Pool application.
Includes encryption, HMAC, display functions, and common helpers.
"""

import sys
import time
import os
import hmac
import hashlib
import base64
import html
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.shortcuts import print_formatted_text
from colorama import Fore, Style, init

init(autoreset=True)

import config


def clear_screen():
    """Clear terminal screen (cross-platform)."""
    os.system('cls' if os.name == 'nt' else 'clear')


def slow_type(text, delay=0.05, color=Fore.YELLOW):
    """Print text with typewriter effect."""
    for char in text:
        sys.stdout.write(color + char)
        sys.stdout.flush()
        time.sleep(delay)
    print(Style.RESET_ALL)


def derive_fernet_key(password: str, salt: bytes, iterations=None):
    """Derive a Fernet key (base64) from password and salt."""
    if iterations is None:
        iterations = config.KDF_ITERATIONS
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def compute_hmac(secret: str, message: bytes) -> bytes:
    """Compute HMAC-SHA256 for authentication."""
    return hmac.new(secret.encode(), message, hashlib.sha256).digest()


def encrypt_ip(plain_ip: str, password: str) -> str:
    """Encrypt server IP address with password.
    
    Returns a compact string: base64salt|base64token
    """
    salt = os.urandom(config.SALT_SIZE)
    key = derive_fernet_key(password, salt)
    f = Fernet(key)
    token = f.encrypt(plain_ip.encode())
    return base64.urlsafe_b64encode(salt).decode() + "|" + base64.urlsafe_b64encode(token).decode()


def decrypt_ip(compound: str, password: str) -> str:
    """Decrypt server IP address with password.
    
    Compound format: base64salt|base64token
    """
    try:
        salt_b64, token_b64 = compound.split("|", 1)
        salt = base64.urlsafe_b64decode(salt_b64)
        token = base64.urlsafe_b64decode(token_b64)
    except Exception as e:
        print_formatted_text(HTML(f'<ansired>Error: Malformed ciphertext.</ansired>'))
        raise

    key = derive_fernet_key(password, salt)
    f = Fernet(key)
    plain = f.decrypt(token)
    return plain.decode()


def get_local_ip() -> str:
    """Get local machine IP address (not 127.0.0.1)."""
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"


def validate_ip(ip: str) -> bool:
    """Validate IPv4 address format."""
    import ipaddress
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ipaddress.AddressValueError:
        return False


def print_banner(text: str, color: str = Fore.MAGENTA):
    """Print colored banner text."""
    print(f"{color}{Style.BRIGHT}{text}{Style.RESET_ALL}")


def print_success(text: str):
    """Print success message in green."""
    print_formatted_text(HTML(f'<b><ansigreen>{html.escape(str(text))}</ansigreen></b>'))


def print_error(text: str):
    """Print error message in red."""
    print_formatted_text(HTML(f'<b><ansired>{html.escape(str(text))}</ansired></b>'))


def print_info(text: str):
    """Print info message in cyan."""
    print_formatted_text(HTML(f'<b><ansicyan>{html.escape(str(text))}</ansicyan></b>'))


def print_warning(text: str):
    """Print warning message in yellow."""
    print_formatted_text(HTML(f'<b><ansiyellow>{html.escape(str(text))}</ansiyellow></b>'))
