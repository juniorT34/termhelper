import os
import requests
from openai import OpenAI
from rich.console import Console
from dotenv import load_dotenv

console = Console()
load_dotenv()

class AIHandler:
    def __init__(self):
        # Load configuration
        self.llm_type = os.getenv("LLM_TYPE", "local")
        
        # OpenAI configuration
        self.openai_key = os.getenv("OPENAI_API_KEY")
        if self.llm_type == "openai" and self.openai_key:
            self.openai_client = OpenAI(api_key=self.openai_key)
            console.print("[green]Using OpenAI for explanations[/green]")
        
        # Local LLM configuration
        self.llm_url = os.getenv("LLM_URL", "http://localhost:11434/api/generate")
        self.llm_model = os.getenv("LLM_MODEL", "codellama")
        if self.llm_type == "local":
            console.print("[green]Using local LLM for explanations[/green]")

    def explain_command(self, command: str) -> str:
        """Get command explanation based on configured LLM."""
        if self.llm_type == "openai" and self.openai_key:
            return self._explain_openai(command)
        return self._explain_local(command)

    def _explain_openai(self, command: str) -> str:
        """Get explanation from OpenAI."""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a Linux command expert. Provide clear, concise explanations with practical examples."},
                    {"role": "user", "content": f"Explain the Linux command: {command}"}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            console.print(f"[red]OpenAI request failed: {str(e)}[/red]")
            return None

    def _explain_local(self, command: str) -> str:
        """Get explanation from local LLM."""
        try:
            prompt = f"Explain the Linux command: {command}\n\nProvide a clear, concise explanation with common usage examples."
            
            response = requests.post(
                self.llm_url,
                json={
                    "model": self.llm_model,
                    "prompt": prompt,
                    "stream": False
                }
            )
            
            if response.status_code == 200:
                return response.json()["response"]
            else:
                console.print(f"[red]Error: API returned status code {response.status_code}[/red]")
                return None
                
        except requests.RequestException as e:
            console.print(f"[red]Error connecting to local LLM: {str(e)}[/red]")
            return None
