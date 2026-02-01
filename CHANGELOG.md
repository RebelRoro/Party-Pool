# Changelog

All notable changes to Party Pool will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-01-23

### Added

#### Core Features
- Multi-user chat server with support for up to 25 concurrent connections
- HMAC-SHA256 authentication (390,000 iterations) with encrypted IP addresses
- Fernet symmetric encryption (AES-based) for secure communications
- Cross-platform support (Windows, Linux, macOS)
- Modular architecture with 90% code duplication elimination

#### Distribution System (NEW)
- **Standalone Package Generation** - Server can create distribution packages for clients and root users
- **Client Package Generation** - Self-contained client with embedded configuration
- **Root Package Generation** - Self-contained admin interface with embedded configuration
- **Windows EXE Generation** - PyInstaller-based executable creation
- **Linux/Mac ZIP Packages** - Cross-platform distribution with setup scripts

#### Root Administrator Features
- Complete administrative command interface:
  - `list` / `help` - Display available commands
  - `close-server` - Shutdown the server gracefully
  - `list-conn` - View all connected clients
  - `remove <username>` - Disconnect specific client
  - `send <message>` - Broadcast message to all clients
  - `exit` - Disconnect root session

#### Client Features
- Full-featured chat client with colored output
- Real-time message receiving (background thread)
- Automatic reconnection prompts on disconnect
- Graceful error handling
- **Client Commands**:
  - `/help` - Display available client commands
  - `/online` - Show list of online users
  - `/ip` - Display your own IP address
  - `/request <message>` - Send request/feedback to admin
  - `/exit` - Disconnect and exit the chat
- Client requests saved to `client_requests.txt` on server

#### Server Features
- Multi-threaded connection handling
- Automatic encrypted IP generation
- Username collision detection
- Broadcast messaging system
- Root command execution

#### Documentation
- Complete README.md with workflow documentation
- QUICKSTART.md - 5-minute setup guide
- INSTALL.md - Platform-specific installation
- CONTRIBUTING.md - Developer guidelines
- RELEASE_NOTES_v1.0.0.md - Version release notes
- CHANGELOG.md - Version history tracking
- Setup scripts (setup.bat/setup.sh) for automated installation

#### Security
- Encrypted IP storage (encrypted_ip.txt)
- Passkey-based client authentication
- Password-based root authentication
- HMAC token verification

### Changed
- License changed from MIT to **CC BY-NC-SA 4.0** (Non-Commercial, ShareAlike)
- Main menu now has 5 options: Start Server, Generate Distribution Packages, Login as Administrator, Login as Client, Exit
- Standalone scripts embed all necessary configuration and utilities
- Package names include version suffix (e.g., `PartyPoolClient-v1.0.0.exe`) to prevent overwrites

### Security Notes
- ⚠️ Change default credentials before deployment
- ⚠️ Only share encrypted_ip.txt with trusted users
- ⚠️ Default port is 12345 (configurable in config.py)

**Full Release Notes**: [RELEASE_NOTES_v1.0.0.md](RELEASE_NOTES_v1.0.0.md)

---

## Versioning Guide

- **Major.Minor.Patch** format (e.g., 1.0.0)
- **Major**: Breaking changes
- **Minor**: New features (backward compatible)
- **Patch**: Bug fixes (backward compatible)

## How to Contribute

Found a bug or have a feature request? See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Note**: This project uses CC BY-NC-SA 4.0 license. Contributions must be non-commercial.

---

*Last Updated: 2026-01-23*
