import requests
from rich.console import Console

console = Console()

def check_ollama():
    """Verify Ollama installation and setup."""
    console.print("\n[bold blue]Checking Ollama Setup...[/bold blue]")
    
    # Check if Ollama is running
    try:
        health = requests.get("http://localhost:11434/api/health")
        console.print("[green]✓ Ollama service is running[/green]")
    except:
        console.print("[red]✗ Ollama service is not running[/red]")
        return False

    # Check model
    try:
        models = requests.get("http://localhost:11434/api/tags")
        if models.status_code == 200:
            model_list = models.json()
            if any(m.get('name') == 'codellama' for m in model_list.get('models', [])):
                console.print("[green]✓ CodeLlama model is installed[/green]")
            else:
                console.print("[yellow]! CodeLlama model not found. Installing...[/yellow]")
                # Try to pull the model
                pull = requests.post("http://localhost:11434/api/pull", json={"name": "codellama"})
                if pull.status_code == 200:
                    console.print("[green]✓ CodeLlama model installed successfully[/green]")
                else:
                    console.print("[red]✗ Failed to install CodeLlama model[/red]")
                    return False
    except Exception as e:
        console.print(f"[red]✗ Error checking models: {str(e)}[/red]")
        return False

    return True

if __name__ == "__main__":
    check_ollama()