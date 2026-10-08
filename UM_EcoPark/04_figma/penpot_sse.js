const TOKEN = process.env.PENPOT_ACCESS_TOKEN;
const URL = "https://design.penpot.app/mcp/stream?userToken=" + TOKEN;

/** Minimal SSE JSON-RPC client: initialize -> notifications/initialized -> call. */
class Penpot {
  async #rpc(session, body, id) {
    const r = await fetch(URL, {
      headers: {
        Accept: "application/json, text/event-stream",
        "Content-Type": "application/json",
        ...(session ? { "mcp-session-id": session } : {}),
      },
      method: "POST",
      body: JSON.stringify({ jsonrpc: "2.0", ...(id ? { id } : {}), ...body }),
    });
    const sid = r.headers.get("mcp-session-id") || session;
    const raw = await r.text();
    for (const line of raw.split("\n")) {
      if (line.startsWith("data: ")) {
        try {
          return { msg: JSON.parse(line.slice(6)), session: sid };
        } catch {}
      }
    }
    return { msg: null, session: sid, raw: raw.slice(0, 400) };
  }

  async connect() {
    const { msg, session } = await this.#rpc(null, {
      method: "initialize",
      params: {
        protocolVersion: "2024-11-05",
        capabilities: {},
        clientInfo: { name: "hermes", version: "1.0.0" },
      },
    }, 1);
    await this.#rpc(session, { method: "notifications/initialized" });
    return { session, tools: msg.result };
  }

  call(session, name, args = {}, id = 2) {
    return this.#rpc(session, { method: "tools/call", params: { name, arguments: args } }, id);
  }

  listTools(session) {
    return this.#rpc(session, { method: "tools/list" }, 2);
  }
}

module.exports = { Penpot, URL, TOKEN };