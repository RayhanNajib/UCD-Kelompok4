const { Penpot } = require("./penpot_sse.js");

const CODE = `
const f = penpot.currentFile;
if (!f) return "NO_FILE";
const pg = penpot.currentPage;
return {
  fileId: f.id,
  fileName: f.name,
  pageId: pg ? pg.id : null,
  pageName: pg ? pg.name : null,
  pages: f.pages.map((p) => ({
    id: p.id,
    name: p.name,
    shapes: p.root ? p.root.children.length : 0,
  })),
  current: pg
    ? pg.root.children.slice(0, 25).map((s) => ({
        id: s.id,
        type: s.type,
        name: s.name || null,
        w: Math.round(s.width),
        h: Math.round(s.height),
      }))
    : [],
};
`;

(async () => {
  const p = new Penpot();
  const { session } = await p.connect();
  const { msg } = await p.call(session, "execute_code", { code: CODE });
  const r = msg.result || {};
  console.log(JSON.stringify(r, null, 1).slice(0, 3500));
})();