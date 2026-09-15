"""Export the approved Beacon Tools identity as a portable, public-safe kit."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
MASTERS = ROOT / "assets/beacon-tools"
KIT = ROOT / "brand-identity/beacon-tools"
NS = "{http://www.w3.org/2000/svg}"
MARK_SIZES = (16, 24, 32, 48, 64, 96, 128, 180, 256, 512, 1024)
LETTERING_WIDTHS = (320, 640, 1280)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def export() -> None:
    if __package__:
        from .sync_brand_v2 import SvgRenderer, write_ico
    else:
        from sync_brand_v2 import SvgRenderer, write_ico

    outputs: set[Path] = set()
    for master in sorted(MASTERS.glob("*.svg")):
        kind = "marks" if "-mark-" in master.name else "lockups"
        target = KIT / "svg" / kind / master.name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(master, target)
        outputs.add(target)

    # Reuse the outlined glyphs from the approved lockup, with their original
    # spacing intact. No font installation is required to use these exports.
    ET.register_namespace("", NS[1:-1])
    for tone in ("ink", "paper"):
        lockup = ET.fromstring((MASTERS / f"beacon-tools-lockup-{tone}.svg").read_bytes())
        width = float(lockup.attrib["viewBox"].split()[2]) - 80
        lettering = ET.Element(NS + "svg", {"viewBox": f"80 0 {width:g} 64"})
        ET.SubElement(lettering, NS + "title").text = "Beacon Tools lettering"
        lettering.append(copy.deepcopy(lockup.findall(NS + "g")[1]))
        target = KIT / "svg/lettering" / f"beacon-tools-lettering-{tone}.svg"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(ET.tostring(lettering, encoding="utf-8"))
        outputs.add(target)

    with SvgRenderer() as renderer:
        for source in sorted(outputs):
            if "-mono." in source.name:
                continue  # currentColor is an SVG-only interface variant.
            mark = source.parent.name == "marks"
            viewbox = ET.fromstring(source.read_bytes()).attrib["viewBox"].split()
            ratio = float(viewbox[3]) / float(viewbox[2])
            for width in MARK_SIZES if mark else LETTERING_WIDTHS:
                height = round(width * ratio)
                target = KIT / "png/transparent" / source.parent.name / f"{source.stem}-{width}.png"
                renderer.render(source, target, width, height)
                outputs.add(target)

        for theme, background, mark_tone, text_tone in (
            ("light", "#f7f8f3", "blue-light", "ink"),
            ("dark", "#17201e", "blue-dark", "paper"),
        ):
            for kind, stem, width in (
                ("marks", f"beacon-tools-mark-{mark_tone}", 512),
                ("lockups", f"beacon-tools-lockup-{theme}", 1280),
                ("lettering", f"beacon-tools-lettering-{text_tone}", 1280),
            ):
                source = KIT / "png/transparent" / kind / f"{stem}-{width}.png"
                target = KIT / f"png/on-{theme}" / f"beacon-tools-{kind}-{width}.png"
                target.parent.mkdir(parents=True, exist_ok=True)
                with Image.open(source) as image:
                    canvas = Image.new("RGBA", image.size, background)
                    canvas.alpha_composite(image.convert("RGBA"))
                    canvas.convert("RGB").save(target)
                outputs.add(target)

    icons = KIT / "icons"
    icons.mkdir(exist_ok=True)
    write_ico(KIT / "png/transparent/marks/beacon-tools-mark-blue-light-512.png", icons / "favicon.ico")
    outputs.add(icons / "favicon.ico")
    for name, size in (("favicon-32.png", 32), ("apple-touch-icon-180.png", 180)):
        target = icons / name
        shutil.copyfile(KIT / f"png/transparent/marks/beacon-tools-mark-blue-light-{size}.png", target)
        outputs.add(target)

    license_path = KIT / "licenses/OFL-DMSans.txt"
    license_path.parent.mkdir(exist_ok=True)
    shutil.copyfile(ROOT / "src/localflight/ui/static/fonts/OFL-DMSans.txt", license_path)
    outputs.add(license_path)
    entries = []
    for file in sorted(outputs):
        item = {"path": file.relative_to(KIT).as_posix(), "sha256": digest(file)}
        if file.suffix == ".png":
            with Image.open(file) as image:
                item.update(width=image.width, height=image.height, transparent="/transparent/" in file.as_posix() or file.parent == icons)
        entries.append(item)
    manifest = {
        "identity": "open-frame-02",
        "sources": [{"path": p.relative_to(ROOT).as_posix(), "sha256": digest(p)} for p in sorted(MASTERS.glob("*.svg"))],
        "outputs": entries,
    }
    (KIT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    check()
    print(f"Exported and verified {len(entries)} brand identity files.")


def check() -> None:
    manifest = json.loads((KIT / "manifest.json").read_text(encoding="utf-8"))
    for item in manifest["sources"]:
        assert digest(ROOT / item["path"]) == item["sha256"], f"Re-export changed master: {item['path']}"
    for item in manifest["outputs"]:
        path = KIT / item["path"]
        assert path.resolve().is_relative_to(KIT.resolve())
        assert digest(path) == item["sha256"], item["path"]
        if path.suffix == ".png":
            with Image.open(path) as image:
                assert image.size == (item["width"], item["height"]), item["path"]
                alpha = image.convert("RGBA").getchannel("A")
                assert alpha.getbbox() is not None, item["path"]
                assert (alpha.getextrema()[0] == 0) == item["transparent"], item["path"]
        elif path.suffix == ".svg":
            svg = ET.fromstring(path.read_bytes())
            assert svg.findall(f".//{NS}path"), item["path"]
            assert svg.find(f".//{NS}text") is None, "Lettering must stay outlined"
    for master in MASTERS.glob("*.svg"):
        kind = "marks" if "-mark-" in master.name else "lockups"
        assert (KIT / "svg" / kind / master.name).read_bytes() == master.read_bytes()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        check()
        print("Brand identity kit hashes, dimensions, transparency and vectors verified.")
    else:
        export()
