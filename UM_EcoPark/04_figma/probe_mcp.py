"""Live smoke test for the Figma MCP server: drives it over stdio with the
official MCP client so tool calls actually round-trip. Run, then read stdout."""

import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER = r"C:\Users\WA\AppData\Local\hermes\skills\figma-mcp\server.py"
PYTHON = r"C:\Users\WA\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe"


async def main() -> None:
    params = StdioServerParameters(command=PYTHON, args=[SERVER])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            print(f"TOOLS {len(tools.tools)}")
            print("NAMES " + " ".join(t.name for t in tools.tools))

            r = await session.call_tool("figma_auth_status", {})
            print("AUTH " + str(r.content[0].text)[:220])

            r2 = await session.call_tool("figma_list_my_files", {})
            print("FILES " + str(r2.content[0].text)[:1400])

            r3 = await session.call_tool(
                "figma_write_bridge",
                {"file_key": "TESTKEY", "ops": '[{"op":"page","name":"Brand Kit"},'
                 '{"op":"frame","name":"Swatches","parent":"Brand Kit","w":400,"h":300,"fill":"#ffffff"},'
                 '{"op":"rect","parent":"Swatches","name":"chip","x":20,"y":20,"w":120,"h":40,'
                 '"fill":"#0f6e3d","radius":12},'
                 '{"op":"text","parent":"Swatches","text":"Primary","x":30,"y":45,"size":14,'
                 '"weight":600,"fill":"#ffffff"}]'},
            )
            print("BRIDGE " + str(r3.content[0].text)[:900])


if __name__ == "__main__":
    asyncio.run(main())