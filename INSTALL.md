# 📦 Installation Guide

Complete installation instructions for Party Pool.

---

## Prerequisites

- **Python 3.8+** (Download: https://www.python.org/downloads/)
- **pip** (Usually included with Python)
- **Git** (Optional, for cloning)

---

## 🖥️ Windows Installation

### Option 1: Using Setup Script (Recommended)
```powershell
git clone https://github.com/vezz-z/party-pool.git
cd party-pool
.\setup.bat
```
The setup script automatically creates a virtual environment and installs all dependencies.

### Option 2: Using Git (Manual)
```powershell
git clone https://github.com/vezz-z/party-pool.git
cd party-pool
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Option 3: Manual Download
1. Download ZIP from https://github.com/vezz-z/party-pool
2. Extract to desired location
3. Open Command Prompt in that folder
4. Run:
```powershell
.\setup.bat
```
Or manually:
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Running on Windows
```powershell
# Activate virtual environment first
venv\Scripts\activate

# Run Party Pool
python main.py
```

---

## 🐧 Linux Installation

### Ubuntu/Debian
```bash
# Install Python if needed
sudo apt update
sudo apt install python3 python3-pip python3-venv git

# Clone and setup using setup script (recommended)
git clone https://github.com/vezz-z/party-pool.git
cd party-pool
chmod +x setup.sh
./setup.sh
```

### Fedora/RHEL
```bash
sudo dnf install python3 python3-pip git
git clone https://github.com/vezz-z/party-pool.git
cd party-pool
chmod +x setup.sh
./setup.sh
```

### Manual Setup (Alternative)
```bash
git clone https://github.com/vezz-z/party-pool.git
cd party-pool
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Running on Linux
```bash
source venv/bin/activate
python3 main.py
```

---

## 🍎 macOS Installation

```bash
# Install Homebrew if needed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python3 git

# Clone and setup using setup script (recommended)
git clone https://github.com/vezz-z/party-pool.git
cd party-pool
chmod +x setup.sh
./setup.sh
```

### Manual Setup (Alternative)
```bash
git clone https://github.com/vezz-z/party-pool.git
cd party-pool
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Running on macOS
```bash
source venv/bin/activate
python3 main.py
```

---

## 📦 Dependencies

The following packages are installed via `requirements.txt`:

| Package | Version | Purpose |
|---------|---------|---------|
| colorama | >=0.4.6 | Colored terminal output |
| cryptography | >=41.0.0 | Encryption functions |
| prompt-toolkit | >=3.0.0 | Advanced CLI input |
| pyinstaller | >=6.0.0 | EXE generation (optional) |

---

## 🔧 Configuration

Before first use, edit `config.py`:

```python
# Change these default passwords!
CLIENT_PASSKEY = "your-secret-passkey"
ROOT_PASSWORD = "your-root-password"
```

---

## 🔥 Firewall Configuration

Party Pool uses port **12345** by default.

### Windows Firewall
```powershell
# Run as Administrator
netsh advfirewall firewall add rule name="Party Pool" dir=in action=allow protocol=TCP localport=12345
```

### Linux (UFW)
```bash
sudo ufw allow 12345/tcp
```

### Linux (firewalld)
```bash
sudo firewall-cmd --permanent --add-port=12345/tcp
sudo firewall-cmd --reload
```

---

## ✅ Verify Installation

Run this command to verify everything works:

```bash
python main.py
```

You should see the Party Pool menu:
```
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║                  🎉 PARTY POOL SERVER 🎉                      ║
║                                                                ║
║                 Multi-Mode Chat Application                    ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝

Please select an option:

  [1] 🖥️ Start Server
  [2] 📦 Generate Distribution Packages
  [3] 🔐 Login as Administrator (Root)
  [4] 💬 Login as Client
  [5] ❌ Exit

════════════════════════════════════════════════════════════════
```

---

## 🆘 Troubleshooting

### "Python not found"
- Ensure Python is in your PATH
- Try `python3` instead of `python`

### "Module not found"
- Activate virtual environment: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Linux/Mac)
- Reinstall dependencies: `pip install -r requirements.txt`

### "Permission denied"
- Linux/Mac: Use `sudo` or fix permissions
- Windows: Run as Administrator

### "Port already in use"
- Change `SERVER_PORT` in `config.py`
- Or kill the process using port 12345

---

## 📚 Next Steps

1. Read [QUICKSTART.md](QUICKSTART.md) for usage instructions
2. Check [README.md](README.md) for full documentation
3. Report issues at https://github.com/vezz-z/party-pool/issues
