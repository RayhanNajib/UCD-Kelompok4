const { Penpot } = require("./penpot_sse.js");

const CODE = `
const page = penpot.currentPage;
const KEEP = ["COPARK / S01 Beranda", "COPARK / S02 Detail Gedung",
  "COPARK / S03 Slot Terpilih", "COPARK / S04 Navigasi",
  "COPARK / S05 Status Kosong", "COPARK / S06 Error Sensor",
  "COPARK / S07 Kualitas Udara"];

// Walk every board once: keep the first of each keep-name, drop the rest
// plus anything left over from the smoke test and the aborted first run.
const seen = new Set();
const removed = [];
for (const s of page.root.children.slice()) {
  const name = String(s.name);
  if (KEEP.includes(name) && !seen.has(name)) {
    seen.add(name);
    continue;
  }
  removed.push(name);
  s.remove();
}
return { kept: Array.from(seen), removedCount: removed.length, removed, pageNow: page.root.children.length };
`;

(async () => {
  const p = new Penpot();
  const { session } = await p.connect();
  const { msg } = await p.call(session, "execute_code", { code: CODE });
  console.log(JSON.stringify(msg.result.content, null, 1).slice(0, 2500));
})();