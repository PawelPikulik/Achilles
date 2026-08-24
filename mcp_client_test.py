"""MCP client test script for FL-05 assignment.

Connects to the filesystem MCP server via stdio and runs three tasks
that chat alone could not do:
1. Read a local file (README.md)
2. List directory contents
3. Write a new file

Run with: python mcp_client_test.py
"""

import asyncio
import sys
from pathlib import Path

# Force UTF-8 for stdout on Windows so README content with BOM prints cleanly
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from mcp import stdio_client
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters
from mcp.types import TextContent

SERVER_PATH = Path(__file__).with_name("mcp_server.py").resolve()


async def run_tasks():
    params = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_PATH)],
    )

    async with stdio_client(params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            init = await session.initialize()
            print(f"=== MCP Server connected: {init.serverInfo.name} ===\n")

            # List available tools
            tools_result = await session.list_tools()
            print("Available tools:")
            for tool in tools_result.tools:
                print(f"  - {tool.name}: {tool.description}")
            print()

            # Task 1: Read a local file
            print("--- TASK 1: read_file (README.md) ---")
            result1 = await session.call_tool("read_file", {"path": str(Path(__file__).parent / "README.md")})
            for content in result1.content:
                if isinstance(content, TextContent):
                    print(content.text[:500] + "..." if len(content.text) > 500 else content.text)
            print()

            # Task 2: List directory contents
            print("--- TASK 2: list_directory (repo root) ---")
            result2 = await session.call_tool("list_directory", {"path": str(Path(__file__).parent)})
            for content in result2.content:
                if isinstance(content, TextContent):
                    print(content.text)
            print()

            # Task 3: Write a new file
            print("--- TASK 3: write_file (mcp_test_output.txt) ---")
            test_path = str(Path(__file__).parent / "mcp_test_output.txt")
            result3 = await session.call_tool("write_file", {
                "path": test_path,
                "content": "MCP test successful. This file was created by the MCP filesystem server, not by chat.\n"
            })
            for content in result3.content:
                if isinstance(content, TextContent):
                    print(content.text)
            print()

            print("=== All three tasks completed. Chat alone cannot do any of these. ===")


if __name__ == "__main__":
    asyncio.run(run_tasks())
