"""Add figures to a gallery: downscale, deduplicate exact pixels, flag similar layouts.

    python scripts/ingest.py <image or folder> ...     # add new figures to gallery-local
    python scripts/ingest.py                           # sync: register images dropped straight into a gallery
    python scripts/ingest.py --gallery gallery <...>   # add to the public gallery

Similar layouts are retained: identical structure does not imply identical data.
Only exact pixel duplicates are skipped. Private ingestion never edits public cards.
New figures get a stub card (appreciated: false) to describe after visual inspection.
"""
import argparse
import hashlib
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cards

# Adapted from liouhai/plot-is-all-you-need (MIT, Copyright 2026 qc).
# See licenses/plot-is-all-you-need-MIT.txt.
MAX_SIDE, G = 2000, 96
MAYBE = 0.55  # approximate layout similarity is a review hint, never grounds to drop data


def _content(im):
    """RGB array with black letterbox and blank margins removed, plus letterbox fraction."""
    im = im.convert("RGB").copy()
    im.thumbnail((640, 640), Image.BOX)
    a = np.asarray(im).astype(np.int16)
    g = a.mean(2)
    r, c = np.where(g.mean(1) >= 35)[0], np.where(g.mean(0) >= 35)[0]
    box = 0.0
    if len(r) and len(c):
        b = a[r[0]:r[-1] + 1, c[0]:c[-1] + 1]
        box = 1 - b.size / a.size
        a = b
    corners = np.concatenate([a[:4, :4].reshape(-1, 3), a[:4, -4:].reshape(-1, 3),
                              a[-4:, :4].reshape(-1, 3), a[-4:, -4:].reshape(-1, 3)])
    ink = np.abs(a - np.median(corners, 0)).max(2) > 22
    r, c = np.where(ink.any(1))[0], np.where(ink.any(0))[0]
    if len(r) > 4 and len(c) > 4:
        a, ink = a[r[0]:r[-1] + 1, c[0]:c[-1] + 1], ink[r[0]:r[-1] + 1, c[0]:c[-1] + 1]
    return a, ink, box


def signature(a):
    """Colour-blind layout signature: edges are taken per channel, so a palette swap keeps them."""
    gx = np.abs(np.diff(a, axis=1, append=a[:, -1:])).max(2)
    gy = np.abs(np.diff(a, axis=0, append=a[-1:])).max(2)
    edge = ((np.maximum(gx, gy) > 18) * 255).astype(np.uint8)
    e = Image.fromarray(edge).resize((G, G), Image.BOX).filter(ImageFilter.GaussianBlur(1))
    s = np.asarray(e, np.float32).ravel()
    s -= s.mean()
    return s / (np.linalg.norm(s) + 1e-9)


def merge_colours(rgb, share, maxn=8, min_share=0.03):
    """Fold near-identical colours together, keep the most common ones. Tints are kept: they are a gradient's steps."""
    rgb, share = np.asarray(rgb, float), np.asarray(share, float).copy()
    alive = np.ones(len(rgb), bool)
    for i in np.argsort(-share):
        if alive[i]:
            for j in range(len(rgb)):
                if j != i and alive[j] and np.linalg.norm(rgb[i] - rgb[j]) < 24:
                    alive[j] = False
                    share[i] += share[j]
    keep = [i for i in np.argsort(-share) if alive[i] and share[i] >= min_share][:maxn]
    return " ".join("#%02x%02x%02x" % tuple(int(v) for v in rgb[i]) for i in keep)


def palette(a, ink):
    """Most common chromatic colours of the figure (greys, near-white and near-black left out)."""
    px = a[ink].reshape(-1, 3)
    px = px[px.max(1) > 45]
    if len(px) < 50:
        return ""
    sat = (px.max(1) - px.min(1)) / np.maximum(px.max(1), 1)
    chrom = px[sat > 0.18]
    if len(chrom) < 0.03 * len(px):
        chrom = px  # greyscale figure
    sub = chrom[np.random.default_rng(0).choice(len(chrom), min(len(chrom), 40000), replace=False)].astype(np.uint8)
    q = Image.fromarray(sub[None]).quantize(16, method=Image.Quantize.MEDIANCUT)
    rgb = np.array(q.getpalette()[:48], float).reshape(-1, 3)
    return merge_colours(rgb, np.bincount(np.asarray(q).ravel(), minlength=len(rgb)) / sub.shape[0])


def same_palette(p, q, tol=18):
    """Two colour lists are the same palette if every colour of each has a close partner in the other."""
    if not p or not q:
        return p == q
    A, B = (np.array([[int(h[k:k + 2], 16) for k in (1, 3, 5)] for h in x.split()], float) for x in (p, q))
    d = np.linalg.norm(A[:, None] - B[None], axis=2)
    return max(d.min(1).mean(), d.min(0).mean()) < tol


def low_quality(im, box):
    w, h = im.size
    return bool(box > 0.05 or abs(w / h - 9 / 16) < 0.01 or max(w, h) < 1000)


def pixels(im):
    """Hash dimensions and RGBA pixels, independent of file name or PNG metadata."""
    rgba = im.convert("RGBA")
    return hashlib.sha256(str(rgba.size).encode() + rgba.tobytes()).hexdigest()


def register(src, gallery, dedup=True, source=""):
    """Returns (status, id, similar_path); never overwrites an image or card."""
    src, gallery = Path(src), Path(gallery)
    gallery.mkdir(parents=True, exist_ok=True)
    ident = src.stem
    dest = gallery / f"{ident}.png"
    in_place = src.parent.resolve() == gallery.resolve()
    if in_place:
        dest = src
    with Image.open(src) as opened:
        im = opened.convert("RGBA")
    digest = pixels(im)
    if not in_place:
        base, serial = ident, 2
        while dest.exists() or dest.with_suffix(".md").exists():
            if dest.exists():
                with Image.open(dest) as old:
                    if pixels(old) == digest:
                        return "exists", ident, None
            ident = f"{base}-{serial}"
            dest = gallery / f"{ident}.png"
            serial += 1
    a, ink, box = _content(im)
    sig, colours = signature(a), palette(a, ink)
    maybe = None
    if dedup:
        best = MAYBE
        galleries = dict.fromkeys([*cards.GALLERIES, gallery])
        for g in galleries:
            for candidate in cards.images(g):
                if candidate.resolve() == src.resolve():
                    continue
                with Image.open(candidate) as existing:
                    meta_path = candidate.with_suffix(".md")
                    meta = cards.read(meta_path)[0] if meta_path.exists() else {}
                    existing_digest = pixels(existing)
                    same_source = (meta.get("source_sha256") == digest and
                                   meta.get("stored_sha256") == existing_digest)
                    if same_source or existing_digest == digest:
                        # A file already dropped into the target directory still needs a card.
                        if not in_place:
                            return "duplicate", ident, str(candidate)
                        maybe = str(candidate)
                    # A short vector reduction avoids platform BLAS float32 warnings.
                    similarity = float(np.sum(signature(_content(existing)[0]) * sig, dtype=np.float64))
                    if similarity > best:
                        best, maybe = similarity, str(candidate)
    if not in_place:
        im = Image.alpha_composite(Image.new("RGBA", im.size, "white"), im).convert("RGB")
        im.thumbnail((MAX_SIDE, MAX_SIDE), Image.LANCZOS)
        im.save(dest, optimize=True)
    card = dest.with_suffix(".md")
    if not card.exists():
        cards.write(card, {"title": "", "kind": "", "purpose": [], "data": "", "loudness": "", "caveat": "",
                           "low_quality": low_quality(im, box), "source": source, "source_sha256": digest,
                           "stored_sha256": pixels(im), "code": "",
                           "appreciated": False, "edited": False, "palettes": [colours] if colours else []})
    return "added", ident, maybe


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--gallery", default="gallery-local")
    ap.add_argument("--no-dedup", action="store_true")
    ap.add_argument("--source", default="")
    args = ap.parse_args()
    gallery = cards.ROOT / args.gallery
    gallery.mkdir(parents=True, exist_ok=True)
    if args.paths:
        todo = [f for p in map(Path, args.paths)
                for f in (sorted(p.iterdir()) if p.is_dir() else [p]) if f.suffix.lower() in cards.IMG_EXT]
    else:  # sync: images dropped straight into the gallery without a card
        todo = [p for p in cards.images(gallery) if not p.with_suffix(".md").exists()]
    added = duplicates = 0
    for f in todo:
        status, ident, other = register(f, gallery, dedup=not args.no_dedup, source=args.source)
        if status == "duplicate":
            duplicates += 1
            print(f"相同图像  {ident} = {other}（跳过，不改动已有卡片）")
        elif status == "added":
            added += 1
            print(f"入库      {ident}" + (f"   ⚠ 可能与 {other} 重复，请对照看一眼" if other else ""))
        else:
            print(f"已存在    {ident}")
    print(f"\n新入库 {added} 张，相同图像 {duplicates} 张。下一步：鉴赏新卡片，然后运行 build_index.py")


if __name__ == "__main__":
    main()
