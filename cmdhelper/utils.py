import os

import yaml
from rich.console import Console
from rich.theme import Theme

from . import config

# Setup colored output
custom_theme = Theme({"desc": "bold green", "cmd": "bold blue", "error": "bold red"})
console = Console(theme=custom_theme)

# Update file paths
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DATA_FILE = os.path.join(DATA_DIR, "commands.yaml")
USER_DATA_FILE = os.path.join(DATA_DIR, "user_commands.yaml")


def load_commands():
    """Load commands from file or cache based on mode."""
    if config.get_offline_mode():
        cache_file = os.path.join(config.CACHE_DIR, config.CACHE_FILE)
        if os.path.exists(cache_file):
            with open(cache_file, "r") as f:
                return yaml.safe_load(f)
        else:
            console.print("[yellow]Warning: No cache found. Loading from files...[/yellow]")

    commands = {}
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            commands.update(yaml.safe_load(f) or {})

    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as f:
            commands.update(yaml.safe_load(f) or {})

    return commands


def add_custom_command(command_desc):
    """Add a custom command to the user commands file."""
    try:
        command, desc = command_desc.split("::")
        user_commands = {}
        if os.path.exists(USER_DATA_FILE):
            with open(USER_DATA_FILE, "r") as f:
                user_commands.update(yaml.safe_load(f) or {})

        if command in user_commands:
            user_commands[command].append(f"{desc}::{command}")
        else:
            user_commands[command] = [f"{desc}::{command}"]

        with open(USER_DATA_FILE, "w") as f:
            yaml.dump(user_commands, f)

        console.print(f"[green]Custom command '{command}' added successfully![/green]")
    except ValueError:
        console.print("[error]Invalid format. Use 'command::description'.[/error]")
    except Exception as e:
        console.print(f"[error]Failed to add custom command: {str(e)}[/error]")
