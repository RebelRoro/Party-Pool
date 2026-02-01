# 🤝 Contributing to Party Pool

Thank you for your interest in contributing to Party Pool! This document provides guidelines and information for contributors.

---

## ⚖️ License Agreement

**Important:** This project is licensed under **CC BY-NC-SA 4.0** (Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International).

By contributing, you agree that:
1. Your contributions will be licensed under the same terms
2. You will not use the code for commercial purposes
3. Any derivative works must also be non-commercial
4. Proper attribution must be maintained

For commercial licensing inquiries, contact: **mohammedparvezofficial@gmail.com**

---

## 🚀 Getting Started

### 1. Fork the Repository
```bash
# Fork on GitHub, then clone your fork
git clone https://github.com/YOUR-USERNAME/party-pool.git
cd party-pool
```

### 2. Set Up Development Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

---

## 📁 Project Structure

```
party-pool/
├── main.py           # Entry point & distribution generator
├── config.py         # Configuration settings
├── requirements.txt  # Dependencies
│
├── server/
│   └── server.py     # Server implementation & root commands
│
├── client/
│   └── client.py     # Client implementation
│
├── root/
│   └── root.py       # Admin interface
│
└── util/
    └── encrypt.py    # Encryption utilities
```

---

## 📝 Code Style Guidelines

### Python Style
- Follow **PEP 8** style guidelines
- Use **4 spaces** for indentation (no tabs)
- Maximum line length: **120 characters**
- Use meaningful variable names

### Naming Conventions
```python
# Classes: PascalCase
class ServerManager:
    pass

# Functions/Methods: snake_case
def handle_client():
    pass

# Constants: UPPER_CASE
MAX_CONNECTIONS = 100

# Private members: leading underscore
def _internal_method():
    pass
```

### Docstrings
```python
def function_name(param1: str, param2: int) -> bool:
    """
    Brief description of what the function does.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    
    Raises:
        ValueError: When invalid input is provided
    """
    pass
```

---

## 🔧 Making Changes

### Adding New Features
1. Create a feature branch from `main`
2. Implement your feature
3. Add/update tests if applicable
4. Update documentation
5. Submit a pull request

### Bug Fixes
1. Create a fix branch from `main`
2. Reference the issue number in commits
3. Include steps to reproduce in PR description
4. Submit a pull request

### Documentation
1. Keep README.md up to date
2. Update CHANGELOG.md for notable changes
3. Add inline comments for complex logic
4. Ensure all public functions have docstrings

---

## 📤 Submitting Pull Requests

### PR Checklist
- [ ] Code follows project style guidelines
- [ ] All existing tests pass
- [ ] New features have documentation
- [ ] CHANGELOG.md updated (if applicable)
- [ ] Branch is up to date with main
- [ ] PR description explains the changes

### PR Title Format
```
[TYPE] Brief description

Types:
- [FEATURE] New functionality
- [FIX] Bug fix
- [DOCS] Documentation only
- [REFACTOR] Code refactoring
- [SECURITY] Security improvement
```

### PR Description Template
```markdown
## Description
Brief description of changes

## Related Issue
Fixes #123

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring
- [ ] Security fix

## Testing
How to test the changes

## Screenshots (if applicable)
```

---

## 🔒 Security

### Reporting Vulnerabilities
If you discover a security vulnerability:
1. **DO NOT** open a public issue
2. Email **mohammedparvezofficial@gmail.com** directly
3. Include detailed description and steps to reproduce
4. Allow time for fix before public disclosure

### Security Guidelines
- Never commit passwords or keys
- Use encryption for sensitive data
- Validate all user inputs
- Follow secure coding practices

---

## 🐛 Bug Reports

### Good Bug Report Includes:
1. **Summary**: Brief description
2. **Environment**: OS, Python version
3. **Steps to Reproduce**: Detailed steps
4. **Expected Behavior**: What should happen
5. **Actual Behavior**: What actually happens
6. **Screenshots/Logs**: If applicable

### Bug Report Template
```markdown
**Environment:**
- OS: Windows 11 / Ubuntu 22.04 / macOS 14
- Python: 3.11.0
- Party Pool Version: 1.0.0

**Steps to Reproduce:**
1. Start server
2. Connect client
3. Do X
4. Error occurs

**Expected:**
Client should receive message

**Actual:**
Connection drops with error: [paste error]

**Logs:**
[paste relevant logs]
```

---

## 💡 Feature Requests

We welcome feature suggestions! Please:
1. Check existing issues for duplicates
2. Provide clear use case
3. Explain why it benefits users
4. Be open to feedback

---

## 📊 Code Review Process

1. At least one maintainer must approve
2. All CI checks must pass
3. No merge conflicts
4. Documentation updated
5. Changelog updated (if applicable)

---

## 📬 Contact

- **Issues**: https://github.com/vezz-z/party-pool/issues
- **Email**: mohammedparvezofficial@gmail.com
- **GitHub**: [@vezz-z](https://github.com/vezz-z)

---

## 🙏 Acknowledgments

Contributors will be recognized in:
- The project README
- Release notes
- CONTRIBUTORS file (for significant contributions)

Thank you for helping make Party Pool better! 🎉
