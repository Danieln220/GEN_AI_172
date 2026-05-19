import asyncio
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

VENV_PYTHON = str(Path(__file__).parent / ".venv" / "Scripts" / "python.exe")

server_params = StdioServerParameters(
    command=VENV_PYTHON,
    args=[str(Path(__file__).parent / "server.py")],
    env=None,
)


def extract_content(payload):
    """Best-effort to pull text from MCP responses."""
    if hasattr(payload, "contents"):
        contents = payload.contents
        if contents:
            first = contents[0]
            if hasattr(first, "text"):
                return first.text
            if isinstance(first, dict) and "text" in first:
                return first["text"]
            return str(first)
    if hasattr(payload, "content"):
        return payload.content
    return str(payload)


async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            resources = await session.list_resources()
            print("Resources:")
            for r in resources.resources:
                print(f"  - {r.uri}")

            templates = await session.list_resource_templates()
            print("Resource templates:")
            for t in templates.resourceTemplates:
                print(f"  - {t.uriTemplate}")

            tools = await session.list_tools()
            print("\nTools:")
            for t in tools.tools:
                print(f"  - {t.name}: {t.description}")

            greeting = await session.read_resource("greeting://hello")
            print(f"\nGreeting: {extract_content(greeting)}")

            result = await session.call_tool("add", arguments={"a": 1, "b": 7})
            print(f"add(1, 7) = {extract_content(result)}")


if __name__ == "__main__":
    asyncio.run(run())
