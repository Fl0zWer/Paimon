# Paimon

Discord bot with web dashboard for server management and features.

## Issue Fix: Missing Dependencies

This repository has been updated to resolve the "⚠️ Sistema .Paimon no disponible en Dashboard: No module named 'aiofiles'" error.

### Quick Fix

```bash
# Install dependencies
pip install -r requirements.txt

# Or use the installation script
./install.sh

# Test dependencies
python3 test_dependencies.py
```

### Dependencies Resolved

- `aiofiles` - Async file operations (main missing dependency)
- `discord.py` - Discord bot library  
- `aiohttp` - Async HTTP client
- `pyttsx3` - Text-to-speech engine
- `python-dotenv` - Environment variables support

### Requirements

- Python 3.11 or later
- Discord bot token
- Proper bot configuration

The missing `aiofiles` dependency has been added to `requirements.txt` along with other necessary packages for the Paimon Discord bot system.