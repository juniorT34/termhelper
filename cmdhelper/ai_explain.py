import os

import openai
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def get_explanation(command):
    prompt = f"""
    Explain the following Linux command in simple terms:

    Command: {command}

    Then provide **two practical examples** of using the command,
    formatted like a real terminal session:

    Example:
    ```
    root@localhost:~# {command} [example usage]\n
    output of the command\n
    ```
    """

    response = openai.chat.completions.create(
        model="gpt-4", messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    print(get_explanation("ls -la"))
