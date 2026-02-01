# 🎉 Party Pool v1.0.0 - Production Ready Release

**Release Date:** January 23, 2026  
**License:** CC BY-NC-SA 4.0 (Non-Commercial)

---

## ✨ Highlights

Party Pool v1.0.0 is a secure, modular, cross-platform chat server with a complete distribution system for sharing standalone client and admin packages.

### 🚀 Key Features

| Feature | Description |
|---------|-------------|
| **Multi-User Chat** | Up to 25 concurrent client connections |
| **Distribution Packages** | Generate standalone packages for clients and admins |
| **Client Commands** | `/help`, `/online`, `/ip`, `/request`, `/exit` |
| **Root Admin Interface** | Complete command system for server management |
| **Cross-Platform** | Windows, Linux, macOS support |
| **Enterprise Encryption** | HMAC-SHA256 + Fernet encryption |

---

## 📦 Distribution System (NEW!)

### What Is It?
The server can now generate **standalone packages** that allow other users to connect without cloning the entire repository.

### Package Types

| Type | Windows | Linux/Mac |
|------|---------|-----------|
| **Client Package** | `.exe` executable | `.zip` with setup scripts |
| **Root Package** | `.exe` executable | `.zip` with setup scripts |

### How It Works

1. **Server starts** → Generates `encrypted_ip.txt`
2. **Server operator** → Creates distribution packages via menu
3. **Packages contain**:
   - Self-contained Python script (client.py or root.py)
   - Embedded encrypted IP configuration
   - Embedded utilities (no external dependencies)
   - requirements.txt
   - Setup scripts (setup.bat / setup.sh)
   - README.txt with instructions
4. **Recipients** → Run setup, then execute the script

---

## 💬 Client Commands

Clients have access to the following commands while connected:

| Command | Description |
|---------|-------------|
| `/help` | Display all available client commands |
| `/online` | Show list of online users |
| `/ip` | Display your own IP address |
| `/request <message>` | Send request/feedback to admin |
| `/exit` | Disconnect and exit Party Pool |

**Requests Feature**: When clients use `/request`, their feedback is saved to `client_requests.txt` on the server with timestamp, username, and IP address for admin review.

---

## 🔧 Root Administrator Commands

Full command interface for server management:

| Command | Description |
|---------|-------------|
| `list` or `help` | Show available commands |
| `close-server` | Shutdown server gracefully |
| `list-conn` | List all connected clients |
| `remove <user>` | Disconnect specific user |
| `send <message>` | Broadcast to all clients |
| `exit` | Close admin session |

---

## 🛡️ Security Features

- ✅ **PBKDF2-HMAC-SHA256** authentication (390,000 iterations)
- ✅ **Fernet encryption** for IP address storage
- ✅ **HMAC token verification** for all connections
- ✅ **Duplicate session prevention**
- ✅ **Encrypted credentials** (.gitignored)

### Security Warnings

⚠️ **Change default credentials in production!**
- Edit `config.py` before deployment
- Change `CLIENT_PASSKEY` and `ROOT_PASSWORD`

⚠️ **Only share encrypted_ip.txt with trusted users**

---

## 📊 Project Metrics

| Metric | Value |
|--------|-------|
| Total Python Files | 11 |
| Lines of Code | ~1,500 |
| Code Duplication | Eliminated 90% |
| Compilation Errors | 0 |
| Import Errors | 0 |

---

## 🚀 Quick Start

### Server Operator

```bash
git clone https://github.com/vezz-z/party-pool.git
cd party-pool
# Windows: .\setup.bat
# Linux/Mac: chmod +x setup.sh && ./setup.sh
python main.py
```

Menu options:
1. **Start Server** - Begins listening for connections
2. **Generate Distribution Packages** - Create client/root packages (Windows EXE or Linux/Mac ZIP)
3. **Login as Administrator (Root)** - Connect to running server as admin
4. **Login as Client** - Connect to server as a chat user
5. **Exit**

### Client User (Using Package)

**Windows (EXE):** Just double-click and run!

**Linux/Mac (ZIP):**
1. Receive package from server operator
2. Extract and run setup script: `chmod +x setup.sh && ./setup.sh`
3. Execute `python3 client.py`
4. Enter passkey when prompted

### Root User (Using Package)

**Windows (EXE):** Just double-click and run!

**Linux/Mac (ZIP):**
1. Receive package from server operator
2. Extract and run setup script: `chmod +x setup.sh && ./setup.sh`
3. Execute `python3 root.py`
4. Enter server passkey, then root password when prompted

---

## 📋 System Requirements

- **Python**: 3.8 or higher
- **OS**: Windows, Linux, or macOS
- **RAM**: Minimum 128MB
- **Network**: Port 12345 accessible

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| cryptography | ≥41.0.0 | Encryption functions |
| colorama | ≥0.4.6 | Colored terminal output |
| prompt-toolkit | ≥3.0.0 | Advanced CLI input |
| pyinstaller | ≥6.0.0 | EXE generation (optional) |

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [README.md](README.md) | Complete feature guide |
| [QUICKSTART.md](QUICKSTART.md) | 5-minute setup |
| [INSTALL.md](INSTALL.md) | Platform installation |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Developer guidelines |
| [CHANGELOG.md](CHANGELOG.md) | Version history |

---

## ⚖️ License

**CC BY-NC-SA 4.0** (Creative Commons Attribution-NonCommercial-ShareAlike 4.0)

- ✅ Free for personal use
- ✅ Free for educational use
- ❌ No commercial use without permission
- 📧 Commercial inquiries: mohammedparvezofficial@gmail.com

---

## 🔗 Links

| Resource | URL |
|----------|-----|
| Repository | https://github.com/vezz-z/party-pool |
| Issues | https://github.com/vezz-z/party-pool/issues |
| Author | [@vezz-z](https://github.com/vezz-z) |

---

## 👨‍💻 Author

**Mohammed Parvez**  
📧 mohammedparvezofficial@gmail.com  
🐙 GitHub: [@vezz-z](https://github.com/vezz-z)

---

## 🎯 What's Next?

Planned for future releases:
- File sharing between clients
- Private messaging (DMs)
- Message history persistence
- Web-based admin dashboard
- Docker deployment support

---

**🎉 Production Ready - Fully tested across Windows, Linux, and macOS**
