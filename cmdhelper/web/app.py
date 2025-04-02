import os
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from rapidfuzz import process
from rich.console import Console

# Add the parent directory to the path to import ai_explain
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cmdhelper.ai_explain import get_explanation
from ..ai_handler import AIHandler

app = Flask(__name__)
console = Console()
ai_handler = AIHandler()


def load_commands():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_file = os.path.join(base_dir, "commands.yaml")
    user_data_file = os.path.join(base_dir, "user_commands.yaml")

    commands = {}
    if os.path.exists(data_file):
        with open(data_file, "r", encoding="utf-8") as f:
            commands.update(yaml.safe_load(f) or {})

    if os.path.exists(user_data_file):
        with open(user_data_file, "r", encoding="utf-8") as f:
            commands.update(yaml.safe_load(f) or {})

    return commands


def check_api_key():
    env_path = os.path.join(str(Path.home()), ".cmdhelper.env")
    load_dotenv(env_path)
    return bool(os.getenv("OPENAI_API_KEY"))


@app.route("/")
def index():
    return render_template("index.html", llm_type=ai_handler.llm_type)


@app.route("/search")
def search():
    query = request.args.get("q", "").strip().lower()
    if not query:
        return jsonify({"error": "Please enter a command"}), 400

    commands = load_commands()

    # Direct match
    if query in commands:
        return jsonify({"command": query, "examples": commands[query]})

    # Fuzzy search
    matches = process.extract(query, commands.keys(), limit=3)
    suggestions = [match[0] for match in matches if match[1] > 60]

    if suggestions:
        return jsonify({"suggestions": suggestions})

    return jsonify({"error": "No matching commands found"})


@app.route("/explain", methods=["POST"])
def explain_command():
    """Handle command explanation requests."""
    try:
        data = request.get_json()
        if not data or 'command' not in data:
            return jsonify({"error": "No command provided"}), 400

        command = data['command']
        console.print(f"[blue]Attempting to explain command: {command}[/blue]")
        
        explanation = ai_handler.explain_command(command)
        if explanation:
            console.print("[green]Successfully generated explanation[/green]")
            return jsonify({"explanation": explanation})
        
        console.print("[red]Failed to generate explanation[/red]")
        return jsonify({"error": "Could not generate explanation"}), 500

    except Exception as e:
        console.print(f"[red]Error in explain_command: {str(e)}[/red]")
        return jsonify({"error": str(e)}), 500


@app.route("/llm-status")
def llm_status():
    status = {
        "type": ai_handler.llm_type,
        "is_openai": ai_handler.llm_type == "openai" and bool(ai_handler.openai_key),
        "model": ai_handler.llm_model if ai_handler.llm_type == "local" else "gpt-3.5-turbo",
    }
    return jsonify(status)


@app.route("/api/status")
def api_status():
    return jsonify({"has_api_key": check_api_key()})


if __name__ == "__main__":
    app.run(debug=True)
