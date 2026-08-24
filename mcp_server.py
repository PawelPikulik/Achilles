"""Simple MCP filesystem server for FL-05 assignment.

Implements three MCP tools that chat alone cannot do:
- read_file: read contents of a local file
- list_directory: list files in a directory
- write_file: create or overwrite a file

Run with: python mcp_server.py
(Used via stdio transport by an MCP client.)
"""

import asyncio
import json
import os
from pathlib import Path

from mcp.server import FastMCP
from mcp.types import TextContent

mcp = FastMCP("filesystem")


@mcp.tool()
async def read_file(path: str) -> str:
    """Read the contents of a file at the given path."""
    try:
        target = Path(path).resolve()
        # Prevent escaping the repo root for safety
        repo_root = Path(__file__).parent.resolve()
        if not str(target).startswith(str(repo_root)):
            return f"Error: Access denied — path outside repo root: {path}"
        content = target.read_text(encoding="utf-8")
        return content
    except Exception as e:
        return f"Error reading {path}: {e}"


@mcp.tool()
async def list_directory(path: str) -> str:
    """List all files and directories at the given path."""
    try:
        target = Path(path).resolve()
        repo_root = Path(__file__).parent.resolve()
        if not str(target).startswith(str(repo_root)):
            return f"Error: Access denied — path outside repo root: {path}"
        entries = sorted(target.iterdir(), key=lambda p: p.name)
        lines = []
        for e in entries:
            kind = "dir" if e.is_dir() else "file"
            lines.append(f"{kind:4} {e.name}")
        return "\n".join(lines) if lines else "(empty directory)"
    except Exception as e:
        return f"Error listing {path}: {e}"


@mcp.tool()
async def write_file(path: str, content: str) -> str:
    """Write content to a file at the given path. Overwrites if exists."""
    try:
        target = Path(path).resolve()
        repo_root = Path(__file__).parent.resolve()
        if not str(target).startswith(str(repo_root)):
            return f"Error: Access denied — path outside repo root: {path}"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return f"Wrote {len(content)} characters to {path}"
    except Exception as e:
        return f"Error writing {path}: {e}"


if __name__ == "__main__":
    asyncio.run(mcp.run_stdio_async())
