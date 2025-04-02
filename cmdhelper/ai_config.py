import os
from enum import Enum
from pathlib import Path


class AIModel(Enum):
    GPT4 = "gpt-4"
    GPT35 = "gpt-3.5-turbo"
    CLAUDE = "claude-3-opus"
    LLAMA = "llama"
    LOCAL = "local"


# AI Model configurations
AI_MODELS = {
    AIModel.GPT4: {
        "name": "GPT-4",
        "provider": "openai",
        "context_length": 8192,
        "requires_key": True,
    },
    AIModel.GPT35: {
        "name": "GPT-3.5",
        "provider": "openai",
        "context_length": 4096,
        "requires_key": True,
    },
    AIModel.CLAUDE: {
        "name": "Claude",
        "provider": "anthropic",
        "context_length": 100000,
        "requires_key": True,
    },
    AIModel.LLAMA: {
        "name": "Llama",
        "provider": "ollama",
        "context_length": 4096,
        "requires_key": False,
    },
    AIModel.LOCAL: {
        "name": "Local LLM",
        "provider": "local",
        "context_length": 2048,
        "requires_key": False,
    },
}

# Default prompts
COMMAND_EXPLAIN_PROMPT = """
Explain the following Linux command in detail:
{command}

Include:
1. Basic purpose
2. Common use cases
3. Important flags/options
4. Potential pitfalls
5. Related commands
"""

NATURAL_LANGUAGE_PROMPT = """
Convert this natural language request into an appropriate Linux command:
{request}

Consider:
1. Best practice approaches
2. Safety considerations
3. Common alternatives
"""

# Environment setup
ENV_FILE = os.path.join(str(Path.home()), ".cmdhelper.env")
