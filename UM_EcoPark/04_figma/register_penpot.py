"""Register the Penpot MCP SSE server in Hermes config without the interactive prompt.

`hermes mcp add --url ... --auth header` blocks on a yes/no question that never
resolves over a pipe, so the entry is written straight into config.yaml instead.
Re-run after rotating the token; it reads the live value from ~/.hermes/.env.
"""

import os
import re
from pathlib import Path

CFG = Path(os.path.expanduser(r"~/AppData/Local/hermes/config.yaml"))
ENV = Path(os.path.expanduser(r"~/.hermes/.env"))


def token() -> str:
    m = re.search(r"^PENPOT_ACCESS_TOKEN=(\S+)", ENV.read_text(encoding="utf-8"), re.M)
    if not m:
        raise SystemExit("PENPOT_ACCESS_TOKEN missing from ~/.hermes/.env")
    return m.group(1)


def main() -> None:
    url = f"https://design.penpot.app/mcp/stream?userToken={token()}"
    block = (
        "  penpot:\n"
        f"    url: {url}\n"
        "    transport: streamable-http\n"
        f"    headers:\n      Authorization: Bearer {token()}\n"
        "    connect_timeout: 90.0\n"
        "    enabled: true\n"
    )
    text = CFG.read_text(encoding="utf-8")
    # drop any stale entry, then insert before the Security section
    text = re.sub(r"\n  penpot:\n(?:[ \t].*\n|\n(?=[ \t]))*", "\n", text)
    anchor = text.index("# ── Security")
    CFG.write_text(text[:anchor] + block + "\n" + text[anchor:], encoding="utf-8")
    print("penpot entry written, url len:", len(url))


if __name__ == "__main__":
    main()