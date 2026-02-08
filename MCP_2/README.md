# MCP Agent with PydanticAI and Google Gemini

A comprehensive implementation of a Model Context Protocol (MCP) agent using PydanticAI and Google's Gemini 2.0 Flash model. This project demonstrates how to build an intelligent agent that can interact with external tools through the MCP protocol.

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [MCP Integration](#mcp-integration)
- [Dependencies](#dependencies)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This project implements an AI agent that leverages:
- **PydanticAI**: A Python framework for building production-grade LLM applications
- **Google Gemini 2.0 Flash**: Google's latest multimodal AI model
- **Model Context Protocol (MCP)**: A standardized protocol for tool integration
- **Weather Tool**: A demonstration MCP server providing weather information

The agent can understand natural language queries and utilize external tools to provide accurate, context-aware responses.

## 🏗️ Architecture
```
    YOU (User) => ask question
            │
            ▼
     🧠 agent.py  ← (THE BRAIN)
            │
            ▼
   🌐 Gemini LLM (Google Cloud)
            │
     decides tool is needed
            │
            ▼
     🔧 weather.py (MCP Tool)
            │
            ▼
        Weather Data
            │
            ▼
        agent.py
            │
            ▼
     Final English Answer
            │
            ▼
            YOU
```

### Architecture Components

1. **User Interface**: Entry point for queries
2. **Agent (agent.py)**: Core orchestration logic
3. **Gemini LLM**: Decision-making and natural language understanding
4. **MCP Server**: Standardized tool interface
5. **Weather Tool**: External data source (example implementation)

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.12 or higher** (specified in `.python-version`)
- **uv** package manager (modern Python package installer)
- **Google Cloud API credentials** with Gemini API access
- **Git** for version control

### System Requirements

- Operating System: Windows, macOS, or Linux
- RAM: Minimum 4GB (8GB recommended)
- Storage: At least 500MB free space
- Internet connection for API calls

## 🚀 Installation

### Step 1: Clone the Repository
```bash
git clone <your-repository-url>
cd MCP_2
```

### Step 2: Install UV Package Manager

If you don't have `uv` installed:
```bash
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Step 3: Set Up Python Environment

The project uses Python 3.12. UV will automatically use the version specified in `.python-version`:
```bash
# UV will create a virtual environment and install dependencies
uv sync
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root:
```bash
# .env
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

To get a Google Gemini API key:
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key to your `.env` file

### Step 5: Update Weather Tool Path

In `agent.py`, update the path to your weather tool:
```python
server = MCPServerStdio(
    command="uv",
    args=[
        "--directory",
        "YOUR_ACTUAL_PATH/weather",  # Update this path
        "run",
        "weather.py",
    ],
)
```

## 📁 Project Structure
```
MCP_2/
├── .python-version          # Python version specification (3.12)
├── agent.py                 # Main agent implementation
├── main.py                  # Entry point (minimal example)
├── pyproject.toml          # Project dependencies and metadata
├── uv.lock                 # Locked dependency versions
├── README.md               # This file
├── .env                    # Environment variables (create this)
│
├── Images/
│   └── production architecture.txt  # Architecture diagram
│
└── weather/                # MCP weather tool (separate project)
    └── weather.py          # Weather tool implementation
```

### Key Files Explained

#### `agent.py`
The core agent implementation that:
- Loads environment variables
- Configures the MCP server connection
- Initializes the Gemini model
- Runs the agent with tool capabilities
```python
import asyncio
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio

# Load environment variables
load_dotenv()

# Configure MCP server
server = MCPServerStdio(
    command="uv",
    args=[
        "--directory",
        "D:\\Genai\\MCP\\weather",
        "run",
        "weather.py",
    ],
)

# Initialize agent with Gemini model
agent = Agent(
    model="google-gla:gemini-2.0-flash",
    toolsets=[server],
)

# Run agent
async def main() -> None:
    async with agent:
        result = await agent.run("What is the trade?")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

#### `pyproject.toml`
Defines project metadata and dependencies:
```toml
[project]
name = "agent"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "httpx>=0.28.1",
    "mcp[cli]>=1.26.0",
    "pydantic-ai-slim[google,mcp]>=1.56.0",
    "python-dotenv>=1.2.1",
]
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Your Google Gemini API key | Yes |

### Model Configuration

The agent uses the following model configuration:
```python
agent = Agent(
    model="google-gla:gemini-2.0-flash",  # Gemini 2.0 Flash model
    toolsets=[server],                     # MCP tools
)
```

### MCP Server Configuration

The MCP server is configured to run a Python script via UV:
```python
server = MCPServerStdio(
    command="uv",                          # Use UV to run
    args=[
        "--directory",
        "/path/to/weather",                # Tool directory
        "run",
        "weather.py",                      # Tool script
    ],
)
```

## 🎮 Usage

### Basic Usage

Run the agent with the default query:
```bash
uv run agent.py
```

### Custom Queries

Modify the query in `agent.py`:
```python
async def main() -> None:
    async with agent:
        result = await agent.run("What is the weather in New York?")
    print(result)
```

### Interactive Mode

You can create an interactive loop:
```python
async def main() -> None:
    async with agent:
        while True:
            query = input("Ask me anything (or 'quit' to exit): ")
            if query.lower() == 'quit':
                break
            result = await agent.run(query)
            print(f"Agent: {result}\n")
```

## 🔧 How It Works

### 1. Initialization Phase
```python
# Load environment variables (API keys, etc.)
load_dotenv()

# Set up MCP server connection
server = MCPServerStdio(...)

# Create agent with model and tools
agent = Agent(
    model="google-gla:gemini-2.0-flash",
    toolsets=[server],
)
```

### 2. Query Processing

When you send a query to the agent:

1. **User Input**: "What is the weather in New York?"
2. **Agent Receives**: Query is sent to the agent's run method
3. **LLM Analysis**: Gemini analyzes the query and determines if tools are needed
4. **Tool Decision**: LLM decides to use the weather tool
5. **Tool Execution**: MCP server executes the weather tool
6. **Data Retrieval**: Weather data is fetched
7. **Response Generation**: LLM formulates a natural language response
8. **User Output**: Final answer is returned

### 3. Async Context Management
```python
async with agent:
    # Agent lifecycle is managed automatically
    result = await agent.run(query)
    # Cleanup happens automatically on exit
```

## 🔌 MCP Integration

### What is MCP?

Model Context Protocol (MCP) is a standardized protocol that enables:
- **Tool Discovery**: Automatically discover available tools
- **Schema Definition**: Define tool inputs and outputs
- **Execution**: Standardized way to call external tools
- **Error Handling**: Consistent error reporting

### MCP Server Communication

The agent communicates with MCP servers via STDIO (standard input/output):
```python
MCPServerStdio(
    command="uv",           # Command to run
    args=[...],            # Arguments to pass
)
```

### Creating Custom MCP Tools

To create your own MCP tool:

1. Create a Python script with tool implementation
2. Define tool schema (inputs, outputs, description)
3. Implement tool logic
4. Configure the tool in your agent

Example tool structure:
```python
# my_tool.py
from mcp import Tool

class MyCustomTool(Tool):
    name = "my_tool"
    description = "Does something useful"
    
    def execute(self, **kwargs):
        # Tool implementation
        return result
```

## 📚 Dependencies

### Core Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `pydantic-ai-slim[google,mcp]` | >=1.56.0 | AI agent framework with Google & MCP support |
| `httpx` | >=0.28.1 | HTTP client for API calls |
| `mcp[cli]` | >=1.26.0 | Model Context Protocol implementation |
| `python-dotenv` | >=1.2.1 | Environment variable management |

### Google Integration

The `[google]` extra installs:
- `google-genai`: Google's Generative AI SDK
- `google-auth`: Authentication for Google services

### MCP Integration

The `[mcp]` extra installs:
- `mcp`: Core MCP protocol implementation
- Tool execution framework
- Schema validation

### Full Dependency Tree

For a complete list of dependencies and their versions, see `uv.lock`.

## 🐛 Troubleshooting

### Common Issues

#### 1. Import Errors

**Problem**: `ModuleNotFoundError: No module named 'pydantic_ai'`

**Solution**:
```bash
# Reinstall dependencies
uv sync --force
```

#### 2. API Key Issues

**Problem**: `Authentication error` or `Invalid API key`

**Solution**:
- Verify your `.env` file exists
- Check that `GOOGLE_API_KEY` is set correctly
- Ensure the API key is valid and not expired
- Verify API is enabled in Google Cloud Console

#### 3. MCP Server Connection Issues

**Problem**: `Failed to connect to MCP server`

**Solution**:
- Verify the weather tool path is correct
- Ensure the weather tool is properly installed
- Check that UV can execute the tool script:
```bash
  uv run --directory /path/to/weather weather.py
```

#### 4. Python Version Issues

**Problem**: `Python version mismatch`

**Solution**:
```bash
# Check Python version
python --version

# Install Python 3.12 if needed
# Then sync with UV
uv sync
```

### Debug Mode

Enable debug logging:
```python
import logging

logging.basicConfig(level=logging.DEBUG)
```

### Getting Help

If you encounter issues:
1. Check the error message carefully
2. Review this troubleshooting section
3. Check the [PydanticAI documentation](https://ai.pydantic.dev/)
4. Check the [MCP documentation](https://modelcontextprotocol.io/)
5. Open an issue on the repository

## 🤝 Contributing

Contributions are welcome! Here's how to contribute:

### Setting Up Development Environment
```bash
# Fork and clone the repository
git clone <your-fork-url>
cd MCP_2

# Create a new branch
git checkout -b feature/your-feature-name

# Install development dependencies
uv sync --all-extras
```

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for functions
- Add tests for new features

### Submitting Changes

1. Ensure all tests pass
2. Update documentation
3. Commit with clear messages
4. Push to your fork
5. Create a pull request

## 📄 License

[Add your license information here]

## 🙏 Acknowledgments

- [PydanticAI](https://ai.pydantic.dev/) - AI agent framework
- [Google Gemini](https://deepmind.google/technologies/gemini/) - LLM provider
- [Model Context Protocol](https://modelcontextprotocol.io/) - Tool integration standard

## 📞 Contact

[Add your contact information here]

---

**Note**: This README assumes you have a working weather MCP tool. If you need help creating one, refer to the MCP documentation or check the examples in the PydanticAI repository.
