"""Render wireframes.html headlessly and assert the sheet actually drew.

Checks that all 7 screens are present at 360x800, that no placeholder leaked
"undefined"/"NaN", and writes a PNG so the result can be eyeballed.
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HTML = "http://localhost:8899/wireframes.html"
SHOT = Path(r"C:\AI AGENT\UM_EcoPark\04_figma\wireframes_sheet.png")


def main() -> int:
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1500, "height": 1000})
        errors: list[str] = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(HTML, wait_until="load")
        page.wait_for_timeout(600)

        data = page.evaluate(
            """() => {
              const figs = [...document.querySelectorAll('figure')];
              return {
                title: document.title,
                count: figs.length,
                captions: figs.map(f => f.querySelector('figcaption')?.childNodes[0]?.textContent.trim()),
                boxes: figs.map(f => {
                  const r = f.querySelector('svg').getBoundingClientRect();
                  return [Math.round(r.width), Math.round(r.height)];
                }),
                shapes: [...document.querySelectorAll('svg')].map(s => s.querySelectorAll('rect,text,circle').length),
                text: document.body.innerText,
              };
            }"""
        )

        page.screenshot(path=str(SHOT), full_page=True)

        text = data["text"]
        bad = [w for w in ("undefined", "NaN", "[object") if w in text]
        sizes_ok = all(b == [360, 800] for b in data["boxes"])

        print(f"title       : {data['title']}")
        print(f"screens     : {data['count']}")
        for cap, box, n in zip(data["captions"], data["boxes"], data["shapes"]):
            print(f"  - {cap:22} {box[0]}x{box[1]}  {n} shapes")
        print(f"sizes 360x800: {sizes_ok}")
        print(f"placeholder leak: {bad or 'none'}")
        print(f"js errors: {errors or 'none'}")
        print(f"screenshot: {SHOT} ({SHOT.stat().st_size} bytes)")

        browser.close()
        ok = data["count"] == 7 and sizes_ok and not bad and not errors
        print("RESULT:", "PASS" if ok else "FAIL")
        return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())