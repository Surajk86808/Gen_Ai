# Weather MCP Server

A Model Context Protocol (MCP) server that provides real-time weather information using the OpenWeatherMap API.

## 📋 Quick Overview

This is a simple MCP server that exposes a weather lookup tool. It can be used with Claude Desktop or any MCP-compatible client to fetch current weather conditions for any city.

## 🚀 Installation

### 1. Clone and Setup
```bash
git clone <your-repo-url>
cd MCP
uv sync
```

### 2. Get API Key
Get a free API key from [OpenWeatherMap](https://openweathermap.org/api)

### 3. Configure Environment
Create `.env` file:
```bash
OPENWEATHER_API_KEY=your_api_key_here
OPENWEATHER_BASE_URL=https://api.openweathermap.org/data/2.5/weather
```

## 🔧 Usage

### Standalone Server
```bash
uv run weather.py
```

### With Claude Desktop
Edit `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "weather": {
      "command": "D:\\path\\to\\MCP\\weather\\.venv\\Scripts\\python.exe",
      "args": ["D:\\path\\to\\MCP\\weather\\weather.py"]
    }
  }
}
```

**Update paths:**
- `command`: Path to your Python executable (venv or UV)
- `args`: Path to `weather.py`

### From Another MCP Client
```python
from pydantic_ai.mcp import MCPServerStdio

server = MCPServerStdio(
    command="uv",
    args=["--directory", "/path/to/weather", "run", "weather.py"]
)
```

## 📦 Dependencies
```toml
python = ">=3.12"
mcp[cli] = ">=1.26.0"
httpx = ">=0.28.1"
requests = ">=2.32.5"
python-dotenv = ">=1.2.1"
```

## 🛠️ How It Works

1. **MCP Server**: Runs via STDIO transport
2. **Tool**: `get_weather(city: str)` - Returns formatted weather string
3. **API**: Fetches data from OpenWeatherMap
4. **Output**: Returns "City: Description, Temperature°C"

## 📁 Project Structure
```
MCP/
├── weather.py              # Main MCP server
├── pyproject.toml         # Dependencies
├── .env                   # API keys (create this)
├── claude_desktop_config.json  # Claude Desktop config
└── README.md
```

## 🔍 Example Usage
```python
# Tool call from Claude or agent
get_weather("London")
# Returns: "London: Clear sky, 15°C"

get_weather("Tokyo")
# Returns: "Tokyo: Partly cloudy, 22°C"
```

## ⚠️ Troubleshooting

**API Key Error**: Verify `.env` has correct `OPENWEATHER_API_KEY`

**Import Error**: Run `uv sync --force`

**Path Error in Config**: Use absolute paths, update for your system

**Server Won't Start**: Check Python version (3.12+)

## 📝 License

[Add your license]

## 🙏 Acknowledgments

- [MCP](https://modelcontextprotocol.io/) - Model Context Protocol
- [OpenWeatherMap](https://openweathermap.org/) - Weather API
