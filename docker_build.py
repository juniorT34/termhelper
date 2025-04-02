import logging
import subprocess
import sys
from pathlib import Path

from rich.console import Console
from rich.live import Live
from rich.logging import RichHandler
from rich.panel import Panel

# Setup rich console
console = Console()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(console=console, rich_tracebacks=True)],
)

log = logging.getLogger("docker_build")


def check_requirements():
    """Check and clean requirements.txt"""
    req_file = Path("requirements.txt")
    if not req_file.exists():
        log.error("requirements.txt not found!")
        return False

    try:
        # Read with UTF-8 encoding
        with open(req_file, "r", encoding="utf-8", errors="ignore") as f:
            requirements = f.readlines()

        # Clean requirements
        cleaned_requirements = []
        for req in requirements:
            # Skip comments and empty lines
            if req.strip() and not req.startswith("#"):
                # Remove any editable install lines
                if not req.startswith("-e"):
                    cleaned_requirements.append(req.strip() + "\n")

        # Write back cleaned requirements
        with open(req_file, "w", encoding="utf-8", newline="\n") as f:
            f.writelines(cleaned_requirements)

        log.info("Requirements file cleaned successfully")
        return True
    except Exception as e:
        log.error(f"Error processing requirements.txt: {str(e)}")
        return False


def build_docker():
    """Build Docker image with live logging"""
    try:
        if not check_requirements():
            return False

        console.rule("[bold blue]Building Docker Image[/bold blue]")

        # Use Popen to stream output in real-time
        process = subprocess.Popen(
            ["docker", "build", "-t", "cmdhelper:latest", "."],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            encoding="utf-8",
            errors="replace",
        )

        # Stream output in real-time
        while True:
            output = process.stdout.readline()
            if output == "" and process.poll() is not None:
                break
            if output:
                console.print(output.strip())

        # Get the return code
        return_code = process.poll()

        if return_code == 0:
            console.print(
                Panel.fit(
                    """[green]🎉 Docker build successful![/green]

To use cmdhelper with Docker, run:
[bold]docker run -it cmdhelper [command][/bold]

Examples:
[bold]docker run -it cmdhelper ls[/bold]
[bold]docker run -it -p 5000:5000 cmdhelper --web[/bold]""",
                    title="Success ✨",
                )
            )
            return True
        else:
            error = process.stderr.read()
            console.print("[red]Docker build failed![/red]")
            console.print(Panel(error, title="Error Output", border_style="red"))
            return False

    except subprocess.CalledProcessError as e:
        log.error(f"Docker build failed: {str(e)}")
        if e.output:
            console.print(
                Panel(
                    e.output.decode("utf-8", errors="replace"),
                    title="Error Output",
                    border_style="red",
                )
            )
        return False
    except Exception as e:
        log.error(f"An unexpected error occurred: {str(e)}")
        return False


if __name__ == "__main__":
    success = build_docker()
    sys.exit(0 if success else 1)
