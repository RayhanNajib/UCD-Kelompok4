"""Drive the Figma MCP server over stdio from a script.

MCP tools only attach at session start, so this is the workaround for the
current session: it speaks MCP to the same server.py over stdio and prints
JSON results. Usage:

    python figma_call.py <tool> '<json-args>' [--raw]
    python figma_call.py <tool> @args.json [--raw]   # args from file

`@args.json` exists because the ops list for a full design run is ~100 KB,
which overruns the Windows 32767-char command-line limit.

    python figma_call.py figma_get_file '{"file_key": "KEY", "depth": 2}'
    python figma_call.py figma_write_bridge @bridge_args.json --raw
"""

import asyncio
import json
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER = r"C:\Users\WA\AppData\Local\hermes\skills\figma-mcp\server.py"
PYTHON = r"C:\Users\WA\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe"


async def call(tool: str, args: dict) -> str:
    params = StdioServerParameters(command=PYTHON, args=[SERVER])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(tool, args)
            return result.content[0].text


def main() -> None:
    tool = sys.argv[1]
    raw_arg = sys.argv[2] if len(sys.argv) > 2 else "{}"
    args = json.loads(Path(raw_arg[1:]).read_text(encoding="utf-8")) \
        if raw_arg.startswith("@") else json.loads(raw_arg)
    raw = "--raw" in sys.argv
    text = asyncio.run(call(tool, args))
    if raw:
        print(text)
        return
    try:
        print(json.dumps(json.loads(text), indent=2, ensure_ascii=False))
    except json.JSONDecodeError:
        print(text)


if __name__ == "__main__":
    main()