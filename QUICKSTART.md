# ⚡ Quick Start Guide

Get Party Pool running in 5 minutes!

---

## 🖥️ Server Setup (Admin)

### Step 1: Clone & Install

**Option A: Using setup scripts (recommended)**
```bash
# Windows
git clone https://github.com/vezz-z/party-pool.git
cd party-pool
setup.bat

# Linux/Mac
git clone https://github.com/vezz-z/party-pool.git
cd party-pool
chmod +x setup.sh && ./setup.sh
```

**Option B: Manual setup**
```bash
# Windows
git clone https://github.com/vezz-z/party-pool.git
cd party-pool
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Linux/Mac
git clone https://github.com/vezz-z/party-pool.git
cd party-pool
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 2: Start Server
```bash
python main.py
# Select [1] Start Server
# Enter your passkey when prompted (remember this for clients!)
```

### Step 3: Generate Packages
```bash
python main.py
# Select [2] Generate Distribution Packages
# Select [3] Both Client & Root
# Select [1] Windows, [2] Linux/macOS, or [3] Both
```

### Step 4: Share
- Send `dist/client/PartyPoolClient-v1.0.0.exe` (or `.zip`) to users
- Send `dist/root/PartyPoolRoot-v1.0.0.exe` (or `.zip`) to admins
- Tell them the passkey (root also needs the root password)
- *(Package names include version suffix to prevent overwriting)*

---

## 💬 Client Setup (End User)

### Windows
1. Receive `PartyPoolClient-v1.0.0.exe` from admin
2. Double-click to run
3. Enter passkey → Enter username → Chat!

### Linux/Mac
1. Receive `PartyPoolClient-v1.0.0.zip`
2. Extract: `unzip PartyPoolClient-v1.0.0.zip`
3. Setup: `chmod +x setup.sh && ./setup.sh`
4. Run: `python3 client.py`

---

## 🔐 Root Admin Setup

### Windows
1. Receive `PartyPoolRoot-v1.0.0.exe` from admin
2. Double-click to run
3. Enter server passkey (same as client passkey)
4. Enter root password
5. Type `list` to see commands

### Linux/Mac
1. Receive `PartyPoolRoot-v1.0.0.zip`
2. Extract: `unzip PartyPoolRoot-v1.0.0.zip`
3. Setup: `chmod +x setup.sh && ./setup.sh`
4. Run: `python3 root.py`
5. Enter passkey → Enter root password → Manage server!

---

## 💬 Client Commands Quick Reference

| Command | What it does |
|---------|--------------|
| `/help` | Show all client commands |
| `/online` | Show online users |
| `/ip` | Show your IP address |
| `/request <msg>` | Send feedback to admin |
| `/exit` | Disconnect and exit |

---

## 📋 Root Commands Quick Reference

| Command | What it does |
|---------|--------------|
| `list` | Show all commands |
| `list-conn` | Show connected users |
| `remove -u alice` | Kick user "alice" |
| `send -all "Hello!"` | Message everyone |
| `close-server` | Shutdown server |
| `exit` | Logout from root |

---

## ⚠️ Important

1. **Change default passwords** in `config.py` before production use:
   - `CLIENT_PASSKEY = "pass"` → your passkey
   - `ROOT_PASSWORD = "toor"` → your root password

2. **Server must be running** before clients can connect

3. **Firewall**: Ensure port 12345 is open

---

## 🆘 Need Help?

- Full documentation: [README.md](README.md)
- Installation guide: [INSTALL.md](INSTALL.md)
- Report issues: https://github.com/vezz-z/party-pool/issues
