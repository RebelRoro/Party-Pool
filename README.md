# 🎉 Party Pool - Multi-User Chat Application

A modular, cross-platform chat server application with administrative controls, secure encryption, and both server and client interfaces.

![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-orange)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20MacOS-blue)
![Encryption](https://img.shields.io/badge/Encryption-HMAC--SHA256-brightgreen)

---

## 🌟 Features

- **Multi-User Chat**: Connect multiple clients to a centralized server (up to 25 concurrent connections)
- **Client Commands**: `/help`, `/online`, `/ip`, `/request`, `/exit` - interactive chat features
- **Server Management**: Root user access with full administrative commands
- **Secure Authentication**: HMAC-SHA256 (390,000 iterations) with encrypted IP addresses
- **Cross-Platform**: Works on Windows, Linux, and macOS
- **Easy Distribution**: Generate standalone packages for clients and administrators
  - **Windows**: Standalone `.exe` executables
  - **Linux/Mac**: ZIP packages with setup scripts
- **Comprehensive Logging**: Detailed server operation logs
- **Thread-Safe**: Handles multiple concurrent connections safely

---

## 📋 System Requirements

- **Python**: 3.8 or higher
- **OS**: Windows, Linux, or macOS
- **RAM**: Minimum 128MB
- **Network**: Local network connectivity

---

## 🚀 Quick Start

### For Server Administrators

#### 1. Clone & Setup

**Windows:**
```bash
git clone https://github.com/vezz-z/party-pool.git
cd party-pool
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Linux / macOS:**
```bash
git clone https://github.com/vezz-z/party-pool.git
cd party-pool
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 2. Start the Server

```bash
python main.py
# Select option [1] Start Server
```

The server will:
1. Prompt for a passkey (this will be used by clients to connect)
2. Generate an encrypted IP file
3. Start listening on port 12345

#### 3. Generate Distribution Packages

```bash
python main.py
# Select option [2] Generate Distribution Packages
```

Choose to generate:
- **Client Package** - For users who want to chat
- **Root Package** - For administrators who need server control
- **Both** - Generate all packages at once

**Output:**
- Windows: `dist/client/PartyPoolClient-v1.0.0.exe` and `dist/root/PartyPoolRoot-v1.0.0.exe`
- Linux/Mac: `dist/client/PartyPoolClient-v1.0.0.zip` and `dist/root/PartyPoolRoot-v1.0.0.zip`

**Note:** Packages are version-suffixed (e.g., `-v1.0.0`) to prevent accidental overwrites between releases.

#### 4. Share with Users

Share the generated packages with your users:
- **Clients** receive the client package (EXE or ZIP)
- **Administrators** receive the root package (EXE or ZIP)

---

### For Chat Clients (End Users)

#### Windows (EXE)
1. Receive `PartyPoolClient-v1.0.0.exe` from the server administrator
2. Double-click to run
3. Enter the passkey provided by the admin
4. Enter your username
5. Start chatting!

#### Linux/Mac (ZIP)
1. Receive `PartyPoolClient-v1.0.0.zip` from the server administrator
2. Extract the ZIP file
3. Run setup to install dependencies:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```
4. Start the client:
   ```bash
   python3 client.py
   ```

---

### For Root Administrators

#### Windows (EXE)
1. Receive `PartyPoolRoot-v1.0.0.exe` from the server administrator
2. Double-click to run
3. Enter the server passkey (same as client passkey)
4. Enter the root password
5. Use commands to manage the server (type `list` for help)

#### Linux/Mac (ZIP)
1. Receive `PartyPoolRoot-v1.0.0.zip`
2. Extract the ZIP file
3. Run setup to install dependencies:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```
4. Start: `python3 root.py`

---

## 🏗️ Project Structure

```
party-pool/
├── main.py                 # Entry point - Main menu & distribution generator
├── config.py               # Centralized configuration
├── requirements.txt        # Python dependencies
├── setup.bat               # Windows setup script (for server administrators)
├── setup.sh                # Linux/macOS setup script (for server administrators)
├── LICENSE                 # CC BY-NC-SA 4.0 License
├── README.md               # This file
│
├── server/
│   ├── __init__.py
│   ├── server.py           # Server implementation with root commands
│   └── tmp/                # Temporary files
│
├── client/
│   ├── __init__.py
│   └── client.py           # Client implementation
│
├── root/
│   ├── __init__.py
│   └── root.py             # Root admin interface
│
├── util/
│   ├── __init__.py         # Package exports
│   ├── common.py           # Shared utilities (encryption, display)
│   ├── encrypt.py          # IP encryption utility
│   └── logger.py           # Logging configuration
│
├── logs/                   # Server logs directory
└── dist/                   # Generated distribution packages
    ├── client/             # Client packages (EXE/ZIP)
    └── root/               # Root packages (EXE/ZIP)
```

### Setup Scripts

| Script | Platform | Purpose |
|--------|----------|---------|
| `setup.bat` | Windows | Automated setup for server administrators - creates venv and installs dependencies |
| `setup.sh` | Linux/macOS | Automated setup for server administrators - creates venv and installs dependencies |

**Note:** The setup scripts included in generated ZIP packages (for clients/root users) are different - they only install minimal dependencies needed to run the standalone scripts.

---

## 🔐 Configuration

All settings are centralized in `config.py`:

```python
# Networking
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 12345

# Application Version
APP_VERSION = "1.0.0"

# Authentication (⚠️ CHANGE IN PRODUCTION!)
CLIENT_PASSKEY = "pass"
ROOT_PASSWORD = "toor"

# Encryption
KDF_ITERATIONS = 390000
SALT_SIZE = 16
```

⚠️ **Security Warning**: Change `CLIENT_PASSKEY` and `ROOT_PASSWORD` in `config.py` before starting the server!

*Changes in the Networking section can be made as you please for further customization.*

---

## 💬 Client Commands Reference

Once connected, clients can use these commands:

| Command | Description |
|---------|-------------|
| `/help` | Display all available commands |
| `/online` | Show list of online users |
| `/ip` | Display your own IP address |
| `/request <message>` | Send a request/feedback to the admin |
| `/exit` | Disconnect and exit Party Pool |

**Note**: Requests are saved to `client_requests.txt` on the server with timestamp, username, and IP for admin review.

---

## 📖 Root Commands Reference

When logged in as root administrator:

| Command | Description |
|---------|-------------|
| `list` | Show all available commands |
| `list-conn` | List all active connections (IP:Username) |
| `list-conn -ip` | List only IP addresses |
| `list-conn -u` | List only usernames |
| `remove -ip <ip>` | Kick user by IP address |
| `remove -u <username>` | Kick user by username |
| `send -all "message"` | Broadcast message to all clients |
| `send -ip <ip1> <ip2> "message"` | Send message to specific IPs |
| `close-server` | Shutdown server immediately |
| `close-server -t 30` | Shutdown server in 30 seconds |
| `close-server -m "Maintenance"` | Shutdown with custom message |
| `exit` | Logout from root session |

---

## 🔄 Workflow Example

### Setting Up a Chat Room

**Step 1: Server Admin starts the server**
```
$ python main.py

  [1] 🖥️ Start Server                    ← Select this
  [2] 📦 Generate Distribution Packages
  [3] 🔐 Login as Administrator (Root)
  [4] 💬 Login as Client
  [5] ❌ Exit

Enter your choice (1-5): 1
Enter passkey: mySecretPass123
✓ Encrypted IP created and saved.
✓ Server started on 0.0.0.0:12345
```

**Step 2: Generate packages for users**
```
$ python main.py
[2] Generate Distribution Packages ← Select this

  [1] 💬 Client Package Only
  [2] 🔐 Root/Admin Package Only
  [3] 📦 Both Client & Root Packages  ← Select this
  [4] 🔙 Back to Main Menu

Enter your choice (1-4): 3

  [1] 🪟 Windows             ← Generates .exe files
  [2] 🐧 Linux/macOS         ← Generates .zip files
  [3] 📦 Both                ← Generates all packages
  [4] 🔙 Back to Main Menu

Enter your choice (1-4): 1
✓ Client EXE created: dist/client/PartyPoolClient-v1.0.0.exe
✓ Root EXE created: dist/root/PartyPoolRoot-v1.0.0.exe
```

**Step 3: Share packages**
- Send `PartyPoolClient-v1.0.0.exe` to chat users
- Send `PartyPoolRoot-v1.0.0.exe` to trusted administrators
- Tell them the passkey: `mySecretPass123` (root also needs root password)

**Step 4: Users connect**
```
# User runs PartyPoolClient-v1.0.0.exe
Enter passkey: mySecretPass123
✓ Authenticated!
Enter username: Alice
✓ Connected as Alice

💬 Connected and Ready!
📝 Type /help for available commands

$Alice: Hello everyone!
$Alice: /online
╔══════════════════════════════════════════╗
║            👥 ONLINE USERS 👥           ║
╠══════════════════════════════════════════╣
║                  Alice                   ║
║                   Bob                    ║
╚══════════════════════════════════════════╝
```

---

## 🛡️ Security Features

- **PBKDF2-HMAC-SHA256**: 390,000 iterations for key derivation
- **Fernet Encryption**: AES-based symmetric encryption for IP addresses
- **HMAC Authentication**: Secure token verification for all connections
- **Duplicate Prevention**: Blocks multiple sessions from same IP
- **Encrypted Credentials**: Server IP is encrypted, not stored in plain text

---

## 📝 Encryption & Security Best Practices

- ✅ Change `CLIENT_PASSKEY` and `ROOT_PASSWORD` before deployment
- ✅ Use strong, unique passwords (12+ characters)
- ✅ Only share distribution packages with trusted users
- ✅ Keep the root password separate from client passkey
- ✅ Monitor `logs/server.log` for suspicious activity

---

## 📜 License

This project is licensed under **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)**.

### You are free to:
- ✅ **Share** — copy and redistribute the material
- ✅ **Adapt** — remix, transform, and build upon the material

### Under the following terms:
- ⚠️ **Attribution** — You must give appropriate credit
- 🚫 **NonCommercial** — You may NOT use for commercial purposes
- 🔄 **ShareAlike** — Modifications must use the same license

For commercial licensing inquiries, contact: mohammedparvezofficial@gmail.com

---

## 📜 Changelog & Releases

See [CHANGELOG.md](CHANGELOG.md) for a history of all releases and updates.

Current version: **[v1.0.0](RELEASE_NOTES_v1.0.0.md)** (Production Ready)

---

## 🙏 Acknowledgments

- Built with Python and modern networking practices
- Uses `cryptography` library for secure encryption
- Inspired by classic chat room applications

---

## 👨‍💻 Author

**Mohammed Parvez**
- Email: mohammedparvezofficial@gmail.com
- GitHub: [@vezz-z](https://github.com/vezz-z)

---

**Made with ❤️ for the community**
