import requests
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Confirm

console = Console()


class OnlineSourceHandler:
    def __init__(self):
        self.tldr_url = "https://raw.githubusercontent.com/tldr-pages/tldr/main/pages/common/{}.md"
        self.timeout = 5

    def show_online_help(self, command: str):
        """Ask user if they want to check TLDR pages"""
        if Confirm.ask("\nWould you like to check TLDR pages for more examples?"):
            self._show_tldr(command)

    def _show_tldr(self, command: str):
        """Show TLDR documentation"""
        try:
            response = requests.get(self.tldr_url.format(command), timeout=self.timeout)
            response.raise_for_status()
            console.print(Panel(Markdown(response.text), title="📚 TLDR Pages", expand=False))
        except requests.RequestException as e:
            console.print(f"[red]Failed to fetch from TLDR: {str(e)}[/red]")
