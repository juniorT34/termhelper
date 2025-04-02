import argparse
import os
import subprocess
from pathlib import Path

import argcomplete
import yaml
from dotenv import load_dotenv, set_key
from rapidfuzz import process
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich.theme import Theme
from rich.panel import Panel

import cmdhelper.update as update

from . import config
from .interactive import interactive_mode
from .online_sources import OnlineSourceHandler
from .utils import add_custom_command, console, load_commands
from .ai_handler import AIHandler

# Setup colored output
custom_theme = Theme({"desc": "bold green", "cmd": "bold blue", "error": "bold red"})
console = Console(theme=custom_theme)

# Update file paths
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DATA_FILE = os.path.join(DATA_DIR, "commands.yaml")
USER_DATA_FILE = os.path.join(DATA_DIR, "user_commands.yaml")


def show_command(command):
    """Display command examples with optional online help."""
    commands = load_commands()

    if command in commands:
        # Show local examples first
        table = Table(title=f"[desc]{command} Examples[/desc]")
        table.add_column("Description", style="desc")
        table.add_column("Command", style="cmd")

        for example in commands[command]:
            try:
                if "::" in example:
                    desc, cmd = example.split("::", 1)
                    table.add_row(desc, cmd.strip("`"))
                else:
                    table.add_row("No description", example)
            except Exception as e:
                console.print(f"[error]Error processing example: {example}[/error]")
                continue

        console.print(table)

        # Offer online sources
        online_handler = OnlineSourceHandler()
        online_handler.show_online_help(command)
    else:
        # Fixed: Properly handle fuzzy matching results
        matches = process.extract(command, commands.keys(), limit=3)
        if matches:
            console.print("[yellow]Did you mean?[/yellow]")
            for match_tuple in matches:
                match_name, score = match_tuple[0], match_tuple[1]
                if score > 60:
                    console.print(f"  - {match_name}")
        else:
            console.print(f"[error]No examples found for '{command}'[/error]")


def run_web():
    """Launch the web app."""
    from cmdhelper.web.app import app

    app.run(debug=True)


def setup_openai_key():
    """Setup OpenAI API key configuration."""
    console.print("[yellow]OpenAI API Key Setup[/yellow]")
    key = console.input("[bold blue]Enter your OpenAI API key: [/bold blue]").strip()

    if not key:
        console.print("[error]Key cannot be empty[/error]")
        return False

    try:
        env_path = os.path.join(str(Path.home()), ".cmdhelper.env")
        set_key(env_path, "OPENAI_API_KEY", key)
        console.print("[green]API key configured successfully![/green]")
        return True
    except Exception as e:
        console.print(f"[error]Failed to save API key: {str(e)}[/error]")
        return False


def check_openai_key():
    """Check if OpenAI API key is configured."""
    env_path = os.path.join(str(Path.home()), ".cmdhelper.env")
    load_dotenv(env_path)
    return bool(os.getenv("OPENAI_API_KEY"))


from enum import Enum


# Define AIModel enumeration
class AIModel(Enum):
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_4 = "gpt-4"
    OPENAI_FREE = "openai-free"


# Define AI_MODELS dictionary
AI_MODELS = {
    "gpt-3.5-turbo": {"name": "GPT-3.5 Turbo", "requires_key": True},
    "gpt-4": {"name": "GPT-4", "requires_key": True},
    "openai-free": {"name": "OpenAI Free Model", "requires_key": False},
}


def configure_ai():
    """Configure AI model preferences."""
    console.print("[bold]Available AI Models:[/bold]")

    for model in AIModel:
        config = AI_MODELS[model]
        requires_key = "🔑" if config["requires_key"] else "🔓"
        console.print(f"{model.value}: {config['name']} {requires_key}")

    choice = Prompt.ask(
        "\n[bold]Choose your preferred model[/bold]",
        choices=[m.value for m in AIModel],
        default="gpt-3.5-turbo",
    )

    try:
        ENV_FILE = os.path.join(str(Path.home()), ".cmdhelper.env")  # Define ENV_FILE
        with open(ENV_FILE, "a") as f:
            f.write(f"\nPREFERRED_AI_MODEL={choice}")
        console.print("[green]AI model preference saved![/green]")
    except Exception as e:
        console.print(f"[red]Failed to save preference: {str(e)}[/red]")


def update_config(key: str, value: str):
    """Update configuration in .env file."""
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    try:
        set_key(env_path, key.upper(), value)
        console.print(f"[green]✓ Updated {key} to {value}[/green]")
    except Exception as e:
        console.print(f"[red]Failed to update config: {str(e)}[/red]")


def parse_config_value(args):
    """Parse configuration value from args."""
    if len(args) == 2:
        key, value = args
        if '=' in key:
            # Handle key=value format
            key, value = key.split('=', 1)
    elif len(args) == 1 and '=' in args[0]:
        # Handle --config key=value format
        key, value = args[0].split('=', 1)
    else:
        raise ValueError("Invalid config format. Use: --config key value or --config key=value")
    return key, value


def main():
    parser = argparse.ArgumentParser(description="Command Helper CLI")
    parser.add_argument("action", nargs="?", help="Action (explain, search, or command name)")
    parser.add_argument("command", nargs="*", help="Command to explain or search")
    parser.add_argument("-i", "--interactive", action="store_true", help="Start interactive mode")
    parser.add_argument("--add", help="Add custom command (format: command::description)")
    parser.add_argument("--offline", action="store_true", help="Enable offline mode")
    parser.add_argument("--cache", action="store_true", help="Update offline cache")
    parser.add_argument("--setup", action="store_true", help="Configure OpenAI API key")
    parser.add_argument("--web", action="store_true", help="Launch web interface")
    parser.add_argument("--config", nargs='+', metavar=('KEY', 'VALUE'), 
                        help="Update configuration (e.g., --config llm.type local or --config llm.type=local)")

    # Enable tab completion
    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    if args.action == "explain":
        if not args.command:
            console.print("[red]Error: Please provide a command to explain[/red]")
            return
        ai_handler = AIHandler()
        command = " ".join(args.command)
        explanation = ai_handler.explain_command(command)
        if explanation:
            console.print(Panel(explanation, title="🤖 AI Explanation"))
        return

    if args.config:
        try:
            key, value = parse_config_value(args.config)
            update_config(key.replace('.', '_'), value)
            return
        except ValueError as e:
            console.print(f"[red]{str(e)}[/red]")
            return

    if args.interactive:
        from .interactive import interactive_mode

        interactive_mode()
        return

    if args.offline:
        config.set_offline_mode(True)
        console.print("[green]Offline mode enabled[/green]")
        return

    if args.cache:
        from .interactive import manage_cache

        manage_cache()
        return

    if args.add:
        add_custom_command(args.add)
        return

    update.update_data()

    if args.action:
        show_command(args.action)
    elif args.web:
        run_web()
    elif args.setup:
        setup_openai_key()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
