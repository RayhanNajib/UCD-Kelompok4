const { Penpot } = require("./penpot_sse.js");
const CODE = `
const out = [];
for (const b of penpot.currentPage.root.children) {
  const kids = b.children;
  const texts = kids.filter((s) => s.type === "text");
  out.push({
    name: b.name,
    size: Math.round(b.width) + "x" + Math.round(b.height),
    rects: kids.filter((s) => s.type === "rectangle").length,
    texts: texts.length,
    firstLine: texts[0] ? texts[0].characters : null,
  });
}
return { boards: out.length, totalShapes: penpot.currentPage.root.children.reduce((a, b) => a + b.children.length, 0), out };
`;
(async () => {
  const p = new Penpot();
  const { session } = await p.connect();
  const { msg } = await p.call(session, "execute_code", { code: CODE });
  console.log(JSON.stringify(msg.result.content, null, 1).slice(0, 3000));
})();
