"""Read/write appreciation cards: `<id>.md` next to `<id>.png`, frontmatter + free text.

Frontmatter is a tiny YAML subset (scalars, inline [a, b] lists, and one dash-list) so the
scripts need no YAML dependency and humans can edit cards in any text editor.
"""
from pathlib import Path

# Adapted from liouhai/plot-is-all-you-need (MIT, Copyright 2026 qc).
# See licenses/plot-is-all-you-need-MIT.txt and references/upstream-integration.md.

ROOT = Path(__file__).resolve().parent.parent
GALLERIES = [ROOT / "gallery", ROOT / "gallery-local"]
IMG_EXT = {".png", ".jpg", ".jpeg", ".webp"}
ORDER = ["title", "kind", "purpose", "data", "loudness", "caveat", "low_quality",
         "source", "code", "appreciated", "edited", "palettes"]
BODY = """**评价**：（待鉴赏）

**部件亮点**
- 结构布局：
- 图形元素：
- 配色：
- 文字与标注：
- 装饰细节：
- 图例与色条：
"""


def _scalar(v):
    v = v.strip()
    if v.startswith("[") and v.endswith("]"):
        return [x.strip().strip("\"'") for x in v[1:-1].split(",") if x.strip()]
    if v in ("true", "false"):
        return v == "true"
    if v.lstrip("-").isdigit():
        return int(v)
    return v.strip("\"'")


def read(path):
    text = Path(path).read_text(encoding="utf-8")
    meta, body = {}, text
    if text.startswith("---"):
        head, _, body = text[3:].partition("\n---")
        key = None
        for line in head.splitlines():
            if line.startswith("  - ") and key:
                meta.setdefault(key, [])
                if not isinstance(meta[key], list):
                    meta[key] = []
                meta[key].append(line[4:].strip().strip("\"'"))
            elif ":" in line:
                key, _, v = line.partition(":")
                key = key.strip()
                meta[key] = _scalar(v) if v.strip() else ""
    return meta, body.lstrip("\n")


def write(path, meta, body=BODY):
    path = Path(path)
    if path.exists() and read(path)[0].get("edited"):
        raise ValueError(f"Refusing to overwrite a user-edited card: {path}")
    out = ["---"]
    for k in ORDER + [k for k in meta if k not in ORDER]:
        if k not in meta:
            continue
        v = meta[k]
        if k == "palettes":
            out.append("palettes:")
            out += [f'  - "{p}"' for p in v]
        elif isinstance(v, list):
            out.append(f"{k}: [{', '.join(v)}]")
        elif isinstance(v, bool):
            out.append(f"{k}: {'true' if v else 'false'}")
        else:
            out.append(f"{k}: {v}")
    Path(path).write_text("\n".join(out) + "\n---\n\n" + body.strip() + "\n", encoding="utf-8")


def images(gallery):
    if not Path(gallery).exists():
        return []
    return sorted(p for p in Path(gallery).iterdir() if p.suffix.lower() in IMG_EXT and not p.name.startswith("."))


def find(ident):
    """Resolve an id (or path) to its image in either gallery."""
    p = Path(ident)
    if p.is_file():
        return p
    matches = []
    for g in GALLERIES:
        for ext in sorted(IMG_EXT):
            if (g / f"{p.stem}{ext}").exists():
                matches.append(g / f"{p.stem}{ext}")
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        raise ValueError(f"Ambiguous gallery id {ident}; supply an explicit image path.")
    raise FileNotFoundError(ident)


if __name__ == "__main__":  # self-check: round trip
    import tempfile
    m = {"title": "环形柱状图: 测试", "kind": "数据图", "purpose": ["比较", "构成"], "loudness": 4,
         "low_quality": False, "code": "", "palettes": ["#aa0000 #00bb00", "#123456 #abcdef"]}
    with tempfile.TemporaryDirectory() as d:
        write(Path(d) / "x.md", m, "正文")
        m2, b = read(Path(d) / "x.md")
    assert m2 == m and b.strip() == "正文", (m2, b)
    print("cards ok")
