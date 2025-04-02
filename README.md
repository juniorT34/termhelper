# Command Helper CLI Tool

A powerful command-line tool to help users find, understand, and learn Linux commands with AI assistance and web interface.

## 📋 Features

- 🔍 Intelligent command search and suggestions
- 🌐 Web interface for easy browsing
- 🤖 AI-powered command explanations (OpenAI/Local LLM)
- 📚 Integration with TLDR pages
- 📦 Docker support
- 💻 Cross-platform (Windows, Linux, macOS)
- ⚡ Interactive shell mode
- 🎯 Custom command support

## 🚀 Installation

### Using Python (Recommended)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install from PyPI
pip install cmdhelper
```

### Using Docker

```bash
# Pull from GitHub Container Registry
docker pull ghcr.io/juniort34/cmdhelper:latest

# Run with Docker
docker run -it cmdhelper --help
```

## ⚙️ Configuration

### AI Setup

#### OpenAI Configuration
1. Get your API key from [OpenAI Platform](https://platform.openai.com)
2. Set up your key:
```bash
cmdhelper --setup
# Enter your OpenAI API key when prompted
```

#### Local LLM Configuration (Optional)
1. Install Ollama:
   - Download from [ollama.ai](https://ollama.ai)
   - Follow installation instructions for your platform
   - Verify installation by running `ollama --version`

2. Pull the CodeLlama model:
```bash
ollama pull codellama
```

3. Create `.env` file in your project root:
```ini
# LLM Configuration
LLM_TYPE=local
LLM_URL=http://localhost:11434/api/generate
LLM_MODEL=codellama
```

4. Configure cmdhelper to use local LLM:
```bash
cmdhelper --config llm.type=local
cmdhelper --config llm.url=http://localhost:11434
cmdhelper --config llm.model=codellama
```

5. Verify setup:
```bash
# Test explanation
cmdhelper explain ls

# Try interactive mode
cmdhelper -i
```

##### Troubleshooting Local LLM

If you encounter issues:

1. Check if Ollama is running:
```bash
# Windows
curl http://localhost:11434/api/generate

# If not running, restart Ollama from Start Menu
```

2. Switch to a different model:
```bash
# Pull lighter model
ollama pull mistral

# Update .env file
LLM_MODEL=mistral
```

3. System Requirements:
- Minimum 8GB RAM
- 2GB free disk space
- CPU with AVX2 support

Note: Local LLM provides:
- 🔒 Full privacy - all processing happens locally
- 🌐 Offline capability
- ⚡ Fast response times
- 🎯 Customizable models

## 🎮 Usage

### Basic Commands
```bash
# Search for a command
cmdhelper ls

# Get AI explanation
cmdhelper explain chmod 755

# Start web interface
cmdhelper --web

# Interactive mode
cmdhelper -i

# Add custom command
cmdhelper --add "mycommand::description"
```

### Interactive Mode
```bash
cmdhelper -i

# Available commands in interactive mode:
? <request>          # Natural language to command
explain <command>    # Get AI explanation
help                 # Show help
exit                 # Exit interactive mode
```

### Web Interface
```bash
# Start web server
cmdhelper --web

# Access via browser
http://localhost:5000
```

### Docker Usage
```bash
# Basic usage
docker run -it cmdhelper ls

# Web interface with port mapping
docker run -it -p 5000:5000 cmdhelper --web

# Interactive mode
docker run -it cmdhelper -i

# With OpenAI key
docker run -it -e OPENAI_API_KEY=your_key cmdhelper
```

## 🛠️ Development

### Setup Development Environment

1. Clone the repository:
```bash
git clone https://github.com/juniort34/cmdhelper.git
cd cmdhelper
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=cmdhelper

# Run specific test file
pytest tests/test_cli.py
```

### Building from Source
```bash
# Build executable
python build.py

# Build Docker image
python docker_build.py
```

## 📁 Project Structure
```
cmdhelper/
├── cmdhelper/          # Main package
│   ├── __init__.py
│   ├── cli.py         # CLI interface
│   ├── web/           # Web interface
│   ├── ai/            # AI handlers
│   └── data/          # Command data
├── tests/             # Test suite
├── requirements.txt   # Dependencies
└── setup.py          # Package setup
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch:
```bash
git checkout -b feature/amazing-feature
```
3. Commit your changes:
```bash
git commit -m 'feat: add amazing feature'
```
4. Push to the branch:
```bash
git push origin feature/amazing-feature
```
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- TLDR pages for command documentation
- OpenAI for AI capabilities
- Rich library for terminal formatting
