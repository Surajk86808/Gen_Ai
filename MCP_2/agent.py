import asyncio
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio


# Load env variables from .env
load_dotenv()

server = MCPServerStdio(
    command="uv",
    args=[
        "--directory",
        "D:\\Genai\\MCP\\weather",
        "run",
        "weather.py",
    ],
)

agent = Agent(
    model="google-gla:gemini-2.0-flash",
    toolsets=[server],
)


async def main() -> None:
    async with agent:
        result = await agent.run("What is the trade?")
        
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
