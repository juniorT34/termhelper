import os
from pathlib import Path

# Configuration for cmdhelper

UPDATE_INTERVAL_DAYS = 7  # Auto-update interval in days
REMOTE_URL = "https://raw.githubusercontent.com/juniorT34/cmdhelper/refs/heads/main/commands.yaml"
CATEGORIES = {
    "file": "File Management",
    "network": "Networking",
    "process": "Process Control",
    "system": "System Administration",
    "git": "Git Commands",
    "docker": "Docker Commands",
    "security": "Security & Permissions",
    "text": "Text Processing",
    "package": "Package Management",
}

# Cache settings
CACHE_DIR = os.path.join(str(Path.home()), ".cmdhelper", "cache")
CACHE_FILE = "commands_cache.json"
OFFLINE_MODE_FILE = os.path.join(CACHE_DIR, "offline_mode")


def get_offline_mode():
    """Check if offline mode is enabled."""
    return os.path.exists(OFFLINE_MODE_FILE)


def set_offline_mode(enabled):
    """Enable or disable offline mode."""
    if enabled:
        if not os.path.exists(CACHE_DIR):
            os.makedirs(CACHE_DIR)
        open(OFFLINE_MODE_FILE, "w").close()
    elif os.path.exists(OFFLINE_MODE_FILE):
        os.remove(OFFLINE_MODE_FILE)


USER_COMMANDS_FILE = "user_commands.yaml"

# UI Settings
DEFAULT_THEME = "dark"
RESULTS_PER_PAGE = 10
