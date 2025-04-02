import os
import time

import requests
from rich.console import Console
from tqdm import tqdm

import cmdhelper.config as config  # Import settings from config.py

console = Console()

# File paths
DATA_FILE = os.path.join(os.path.dirname(__file__), "commands.yaml")
UPDATE_CHECK_FILE = os.path.join(os.path.dirname(__file__), "last_update.txt")


def time_since_last_update():
    """Check how many days have passed since the last update."""
    if not os.path.exists(UPDATE_CHECK_FILE):
        return float("inf")  # If no record exists, force an update

    with open(UPDATE_CHECK_FILE, "r") as f:
        try:
            last_update_time = float(f.read().strip())
        except ValueError:
            return float("inf")

    return (time.time() - last_update_time) / 86400  # Convert seconds to days


def save_update_time():
    """Record the current time as the last update time."""
    with open(UPDATE_CHECK_FILE, "w") as f:
        f.write(str(time.time()))


def fetch_data_with_progress(url, destination):
    """Download file with a progress bar."""
    try:
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get("content-length", 0))

        if response.status_code == 200:
            with open(destination, "wb") as f, tqdm(
                desc="Downloading", total=total_size, unit="B", unit_scale=True, unit_divisor=1024
            ) as bar:
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)
                    bar.update(len(chunk))
            return True
        else:
            console.print(f"[red]Failed to fetch data (HTTP {response.status_code}).[/red]")
            return False
    except requests.RequestException as e:
        console.print(f"[red]Update failed: {e}[/red]")
        return False


def update_data(force=False):
    """Check if an update is needed, then fetch the latest command examples."""
    if not force and time_since_last_update() < config.UPDATE_INTERVAL_DAYS:
        console.print(
            f"[yellow]Skipping update. Last update was within {config.UPDATE_INTERVAL_DAYS} days.[/yellow]"
        )
        return

    console.print("[cyan]Fetching latest command data...[/cyan]")
    if fetch_data_with_progress(config.REMOTE_URL, DATA_FILE):
        save_update_time()
        console.print("[green]Command data updated successfully![/green]")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Update command database")
    parser.add_argument("--force", action="store_true", help="Force update even if it's not due")
    args = parser.parse_args()

    update_data(force=args.force)
