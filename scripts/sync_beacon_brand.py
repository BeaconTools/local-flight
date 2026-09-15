"""Synchronize Open Frame artwork from the committed Beacon Tools SVG masters.

Local Flight product icons and historical product screenshots are independent.
Run this after updating the masters; --check verifies the recorded output hashes.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import html
import json
import re
import shutil
from pathlib import Path

from PIL import Image

from sync_brand_v2 import SvgRenderer, write_ico

ROOT = Path(__file__).resolve().parents[1]
MASTERS = ROOT / "assets/beacon-tools"
SITE = ROOT / "site/public/assets"
STATIC = ROOT / "src/localflight/ui/static"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sync() -> None:
    outputs: set[Path] = set()
    for source in sorted(MASTERS.glob("*.svg")):
        for target in (SITE / source.name, STATIC / source.name):
            shutil.copyfile(source, target)
            outputs.add(target)
    mono = (MASTERS / "beacon-tools-mark-mono.svg").read_text()
    body = re.sub(r"^.*?</title>", "", mono, flags=re.S).removesuffix("</svg>")
    inline = '<svg viewBox="0 0 64 64" fill="currentColor" aria-hidden="true">' + body + '</svg>'
    frame_path = re.search(r'<path d="([^"]+)"', mono).group(1)
    (ROOT / "mobile/src/theme/beaconBrand.ts").write_text(
        '// Open Frame master: assets/beacon-tools/beacon-tools-mark-mono.svg\n'
        + 'export const BEACON_FRAME_PATH = ' + json.dumps(frame_path) + ';\n', encoding="utf-8"
    )
    with SvgRenderer() as renderer:
        for name, size, master in (
            ("beacon-tools-mark-96.png", 96, "blue-light"),
            ("beacon-tools-mark-dark-96.png", 96, "blue-dark"),
            ("beacon-tools-icon-512.png", 512, "blue-light"),
            ("apple-touch-icon.png", 180, "blue-light"),
            ("favicon-32.png", 32, "blue-light"),
        ):
            target = SITE / name
            renderer.render(MASTERS / f"beacon-tools-mark-{master}.svg", target, size, size)
            outputs.add(target)
        renderer.render(MASTERS / "beacon-tools-lockup-dark.svg", SITE / "beacon-tools-logo.png", 1200, 349)
        outputs.add(SITE / "beacon-tools-logo.png")
        write_ico(SITE / "beacon-tools-icon-512.png", SITE / "favicon.ico")
        outputs.add(SITE / "favicon.ico")

        # Current rendition gallery keeps its established URLs.
        gallery = ROOT / "docs/brand-renditions/v2/images"
        for target in sorted(gallery.glob("beacon-*.png")):
            if "contact-sheet" in target.name:
                continue
            with Image.open(target) as old:
                width, height = old.size
            dark = "on-dark" in target.name
            kind = "mark" if "beacon-mark" in target.name else "lockup"
            suffix = ("blue-dark" if dark else "blue-light") if kind == "mark" else ("dark" if dark else "light")
            renderer.render(MASTERS / f"beacon-tools-{kind}-{suffix}.svg", target, width, height)
            if "on-dark" in target.name or "on-light" in target.name:
                with Image.open(target) as rendered:
                    canvas = Image.new("RGBA", rendered.size, "#17201e" if dark else "#f7f8f3")
                    canvas.alpha_composite(rendered.convert("RGBA"))
                    canvas.save(target)
            outputs.add(target)
        for target in (gallery / "beacon-mark-size-contact-sheet.png", gallery / "brand-overview-contact-sheet.png"):
            with Image.open(target) as old:
                width, height = old.size
            canvas = Image.new("RGBA", (width, height), "#f7f8f3")
            if "size" in target.name:
                with Image.open(SITE / "beacon-tools-icon-512.png") as mark:
                    sizes = (16, 32, 64, 96, 180, 256)
                    for i, size in enumerate(sizes):
                        canvas.alpha_composite(mark.resize((size, size), Image.Resampling.LANCZOS), (int((i + .5) * width / len(sizes) - size / 2), (height - size) // 2))
            else:
                # Retain Local Flight in the combined family overview.
                for i, source in enumerate((gallery / "beacon-lockup-on-light-1280x420.png", ROOT / "assets/icon.png")):
                    with Image.open(source) as item:
                        item = item.convert("RGBA")
                        item.thumbnail((int(width * .82), int(height * .38)), Image.Resampling.LANCZOS)
                        canvas.alpha_composite(item, ((width - item.width) // 2, int(height * (.08 if i == 0 else .55))))
            canvas.save(target)
            outputs.add(target)

    landing = ROOT / "relay/public/index.html"
    text = landing.read_text(encoding="utf-8")
    light = base64.b64encode((SITE / "beacon-tools-mark-96.png").read_bytes()).decode()
    dark = base64.b64encode((SITE / "beacon-tools-mark-dark-96.png").read_bytes()).decode()
    picture = f'<picture class="beacon-picture"><source media="(prefers-color-scheme: dark)" srcset="data:image/png;base64,{dark}"><img class="brand-mark" src="data:image/png;base64,{light}" alt="" width="44" height="44"></picture>'
    text = re.sub(r'<picture class="beacon-picture">.*?</picture>|<img class="brand-mark"[^>]*>', lambda _: picture, text, count=1, flags=re.S)
    landing.write_text(text, encoding="utf-8")
    for name in ("relay/admin/admin.html", "relay/main.py", "src/localflight/ui/templates/admin.html"):
        path = ROOT / name
        text = path.read_text(encoding="utf-8")
        text = re.sub(r'<!-- BEACON_MARK -->.*?<!-- /BEACON_MARK -->', lambda _: '<!-- BEACON_MARK -->' + inline + '<!-- /BEACON_MARK -->', text, flags=re.S)
        path.write_text(text, encoding="utf-8")

    manifest_path = ROOT / "assets/brand-manifest.json"
    manifest = json.loads(manifest_path.read_text())
    known = {item["path"] for item in manifest["active_outputs"]}
    for target in sorted(outputs):
        relative = target.relative_to(ROOT).as_posix()
        if relative not in known:
            manifest["active_outputs"].append({"role": "beacon-open-frame", "path": relative, "width": None, "height": None, "sha256": digest(target)})
    for item in manifest["active_outputs"]:
        target = ROOT / item["path"]
        if target in outputs:
            item["sha256"] = digest(target)
    manifest["masters"].update(beacon_lockup="repository-open-frame-lockup", beacon_mark="repository-open-frame-mark")
    manifest["beacon_identity"] = "open-frame-02"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    rendition_path = ROOT / "docs/brand-renditions/v2/manifest.json"
    rendition = json.loads(rendition_path.read_text())
    def refresh(value: object) -> None:
        if isinstance(value, dict):
            for child in value.values():
                refresh(child)
            if "path" in value and "sha256" in value:
                candidate = ROOT / str(value["path"])
                if candidate.is_file() and candidate in outputs:
                    value["sha256"] = digest(candidate)
        elif isinstance(value, list):
            for child in value:
                refresh(child)
    refresh(rendition)
    rendition["masters"].update(beacon_lockup="repository-open-frame-lockup", beacon_mark="repository-open-frame-mark")
    cards = []
    for item in rendition["renditions"]:
        target = rendition_path.parent / item["file"]
        if target in outputs:
            item["sha256"] = digest(target)
            item["source"] = "repository-open-frame"
        file = html.escape(item["file"], quote=True)
        title = html.escape(item["title"])
        cards.append(f'<article><a href="{file}"><img src="{file}" alt="{title}" loading="lazy"></a><h2>{title}</h2><p>{item["width"]} × {item["height"]}</p></article>')
    gallery_html = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Beacon Tools / Local Flight — Brand artwork</title><style>
    :root{color-scheme:light dark}*{box-sizing:border-box}body{margin:0;background:#f7f8f3;color:#202b29;font:16px/1.6 "DM Sans",system-ui,sans-serif}main{max-width:1180px;margin:auto;padding:40px 24px}h1{font-weight:500;letter-spacing:-.04em}p{color:#58655f}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:18px}article{border:1px solid #b6c0b2;border-radius:10px;padding:14px;min-width:0}img{width:100%;height:180px;object-fit:contain;background:#edf0e7;border-radius:7px}h2{font-size:15px}a{color:inherit}:focus-visible{outline:3px solid #315bd6;outline-offset:4px}@media(prefers-color-scheme:dark){body{background:#17201e;color:#f3f5ed}p{color:#abb9ae}article{border-color:#47594b}}
    </style></head><body><main><h1>Beacon Tools / Local Flight</h1><p>Current Open Frame studio artwork and retained Local Flight product identity. The established gallery URLs remain available.</p><p><a href="../../brand-guide.md">Brand guide</a></p><section class="grid">'''
    (rendition_path.parent / "index.html").write_text(gallery_html + "".join(cards) + "</section></main></body></html>", encoding="utf-8")
    rendition_path.write_text(json.dumps(rendition, indent=2) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        manifest = json.loads((ROOT / "assets/brand-manifest.json").read_text())
        for item in manifest["active_outputs"]:
            if "beacon" in item["role"] or "beacon" in item["path"]:
                assert digest(ROOT / item["path"]) == item["sha256"], item["path"]
        for master in MASTERS.glob("*.svg"):
            for target in (SITE / master.name, STATIC / master.name):
                assert target.read_bytes() == master.read_bytes(), target.name
        print("Beacon Tools canonical vectors and recorded outputs verified.")
    else:
        sync()
        print("Beacon Tools Open Frame assets synchronized.")


if __name__ == "__main__":
    main()
