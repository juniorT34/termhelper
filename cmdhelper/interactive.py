import os
from pathlib import Path

import yaml
from rapidfuzz import process
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from . import config
from .ai_handler import AIHandler
from .utils import add_custom_command, console, load_commands


class InteractiveShell:
    def __init__(self):
        self.ai_handler = AIHandler()

    def start(self):
        """Start the interactive shell."""
        console.print(
            Panel.fit(
                "[bold green]Welcome to Command Helper Interactive Mode![/bold green]\n"
                "Type [bold cyan]help[/bold cyan] to see available commands, [bold cyan]exit[/bold cyan] to quit"
            )
        )

        while True:
            try:
                cmd = Prompt.ask("\n[bold blue]cmdhelper>[/bold blue]").strip()

                if not cmd:
                    continue

                if cmd == "exit":
                    console.print("[yellow]Goodbye![/yellow]")
                    break

                self.handle_command(cmd)

            except KeyboardInterrupt:
                console.print("\n[yellow]Use 'exit' to quit[/yellow]")
            except Exception as e:
                console.print(f"[red]Error: {str(e)}[/red]")

    def handle_command(self, cmd: str):
        """Handle different command inputs."""
        if cmd == "help":
            self.show_help()
        elif cmd == "clean" or cmd == "cls":
            os.system('cls' if os.name == 'nt' else 'clear')
        elif cmd.startswith("?"):
            # Natural language query
            request = cmd[1:].strip()
            if request:
                response = self.ai_handler.natural_to_command(request)
                console.print(Panel(response, title="AI Generated Command"))
            else:
                console.print("[yellow]Usage: ? <what you want to do>[/yellow]")
        elif cmd.startswith("explain "):
            # Explicit command explanation
            command = cmd[8:].strip()
            if command:
                response = self.ai_handler.explain_command(command)
                console.print(Panel(response, title=f"Explanation for '{command}'"))
            else:
                console.print("[yellow]Usage: explain <command>[/yellow]")
        elif cmd.startswith("add "):
            # Add custom command
            command = cmd[4:].strip()
            if command:
                desc = Prompt.ask("[cyan]Enter command description[/cyan]")
                if desc:
                    add_custom_command(f"{command}::{desc}")
                    console.print(f"[green]Added custom command: {command}[/green]")
                else:
                    console.print("[yellow]Description cannot be empty[/yellow]")
            else:
                console.print("[yellow]Usage: add <command>[/yellow]")
        else:
            show_command(cmd)

    def show_help(self):
        """Display help information."""
        help_table = Table(show_header=True)
        help_table.add_column("Command", style="cyan")
        help_table.add_column("Description", style="green")

        help_table.add_row("? <request>", "Convert natural language to command")
        help_table.add_row("explain <command>", "Get AI explanation for command")
        help_table.add_row("add <command>", "Add a custom command")
        help_table.add_row("clean", "Clear the screen")  # New row
        help_table.add_row("help", "Show this help message")
        help_table.add_row("exit", "Exit interactive mode")
        help_table.add_row("<command>", "Search for a command")

        console.print(Panel(help_table, title="Available Commands"))


def interactive_mode():
    """Start interactive mode."""
    shell = InteractiveShell()
    shell.start()


def show_command(command):
    """Display command examples in interactive mode."""
    commands = load_commands()

    if command in commands:
        table = Table(title=f"[desc]{command} Examples[/desc]")
        table.add_column("Description", style="desc")
        table.add_column("Command", style="cmd")

        for example in commands[command]:
            try:
                # Handle example format safely
                if "::" in example:
                    desc, cmd = example.split("::", 1)  # Split on first :: only
                    table.add_row(desc, cmd.strip("`"))  # Remove backticks if present
                else:
                    # Handle malformed example
                    table.add_row("No description", example)
            except Exception as e:
                console.print(f"[error]Error processing example: {example}[/error]")
                continue

        console.print(table)
    else:
        matches = process.extract(command, commands.keys(), limit=3)
        if matches:
            console.print("[yellow]Did you mean?[/yellow]")
            for match in matches:
                if match[1] > 60:  # Check similarity score
                    console.print(f"  - {match[0]}")
        else:
            console.print(f"[error]No examples found for '{command}'[/error]")
