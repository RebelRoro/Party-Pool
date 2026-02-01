"""
IP Encryption utility for server-client secure authentication.
Uses shared common module for encryption functions.
"""

from util.common import encrypt_ip, get_local_ip


def init_encrypt():
    """Initialize encryption process for server IP."""
    local_ip = get_local_ip()
    passwd = input("Enter passkey (will be used to decrypt on client): ").strip()
    ct = encrypt_ip(local_ip, passwd)
    return ct
    