"""Put the UM EcoPark SVG screens on the Windows clipboard as one SVG payload.

Figma turns pasted SVG into real vector layers, not a flat image, so this is the
clipboard route into a Figma file that needs no mouse: write the clipboard, then
send Ctrl+V into the canvas.

Two payloads are used:
  - one SVG containing every frame laid out in a row, for a single paste
  - one SVG per screen, for pasting them one at a time

Run:  python figma_clip.py <mode> [out_name]
      mode = combined | single
"""

import sys
from pathlib import Path

WF = Path(r"C:\AI AGENT\UM_EcoPark\01_wireframe")
MF = Path(r"C:\AI AGENT\UM_EcoPark\03_medium_fi")

GAP = 40


def read_svg(p: Path) -> str:
    """Strip the XML declaration and pull out width/height/viewBox."""
    t = p.read_text(encoding="utf-8")
    if t.startswith("<?xml"):
        t = t[t.index("?>") + 2:].lstrip()
    return t


def dims(svg: str) -> tuple[int, int]:
    import re
    w = re.search(r'\bwidth="([\d.]+)"', svg)
    h = re.search(r'\bheight="([\d.]+)"', svg)
    return int(float(w.group(1))), int(float(h.group(1)))


def combine(paths: list[Path]) -> str:
    """Wrap each screen in a <g transform> inside one wide canvas."""
    parts, x = [], 0
    for p in paths:
        svg = read_svg(p)
        w, h = dims(svg)
        body = svg[svg.index(">") + 1:]
        body = body[: body.rindex("</svg>")]
        # a white plate per frame so each screen keeps its own background
        parts.append(
            f'<g transform="translate({x},0)">'
            f'<rect x="0" y="0" width="{w}" height="{h}" fill="#ffffff"/>'
            f"{body}</g>"
        )
        x += w + GAP
    total_w, total_h = max(dims(read_svg(p)) for p in paths)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{x - GAP}" '
        f'height="{total_h}" viewBox="0 0 {x - GAP} {total_h}">'
        + "".join(parts)
        + "</svg>"
    )


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else "combined"
    out = Path(r"C:\AI AGENT\UM_EcoPark\04_figma") / (
        "clip_combined.svg" if mode == "combined" else "clip_single.svg"
    )
    if mode == "combined":
        paths = sorted(MF.glob("*.svg")) + sorted(WF.glob("*.svg"))
        svg = combine(paths)
        out.write_text(svg, encoding="utf-8")
        print(f"{out}  {len(svg)} bytes  ({len(paths)} screens combined)")
    else:
        for p in sorted(MF.glob("*.svg")):
            (out.parent / f"clip_{p.stem}.svg").write_text(p.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"wrote {len(sorted(MF.glob('*.svg')))} single-screen SVGs next to {out.name}")


if __name__ == "__main__":
    main()