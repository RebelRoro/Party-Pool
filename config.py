"""
Centralized configuration for Party Pool application.
Stores all constants, defaults, and shared settings.
"""

import os

# ===== NETWORKING =====
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 12345
BUFFER_SIZE = 8192

# ==== TIMEOUTS & LIMITS =====
# Edit as you see fit
# SERVER_TIMEOUT = 30
# MAX_CONNECTIONS = 25 # Comment line 533 in server/server.py and uncomment line 534 to change

# ===== AUTHENTICATION & ENCRYPTION =====
AUTH_MESSAGE = b"party-pool-auth-v1.0.0"
ROOT_AUTH = b"root-auth-key-v1.0.0"
ILLEGAL_CHARS = ['<', '>']
KDF_ITERATIONS = 390000
SALT_SIZE = 16

# ===== PASSWORDS (Should be changed in production) =====
CLIENT_PASSKEY = "pass"
ROOT_PASSWORD = "toor"

# ===== LOGGING =====
LOG_DIR = "logs"
SERVER_LOG = os.path.join(LOG_DIR, "server.log")
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_LEVEL = "INFO"

# ===== PATHS =====
ENCRYPTED_IP_FILE = "encrypted_ip.txt"

# ===== APPLICATION NAMES =====
APP_NAME = "Party Pool"
APP_VERSION = "1.0.0"
CLIENT_EXE_NAME = "PartyPoolClient"
CLIENT_ICON_FILE = "client_icon.png"
ROOT_EXE_NAME = "PartyPoolRoot"
ROOT_ICON_FILE = "root_icon.png"

# ===== MESSAGES =====
WELCOME_MSG = "Welcome to Party Pool!"
GOODBYE_MSG = "Goodbye from Party Pool!"
AUTH_FAILED_MSG = "Authentication failed"
CONNECTION_CLOSED_MSG = "Server connection closed"

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)
