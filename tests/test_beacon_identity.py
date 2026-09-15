"""Keep the studio's independent renderers tied to the approved vector masters."""
from __future__ import annotations

import base64
import hashlib
import json
import re
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
MASTERS = ROOT / "assets/beacon-tools"


def test_public_and_packaged_studio_vectors_match_the_canonical_artwork():
    for master in MASTERS.glob("*.svg"):
        ET.fromstring(master.read_bytes())
        for directory in ("site/public/assets", "src/localflight/ui/static"):
            assert (ROOT / directory / master.name).read_bytes() == master.read_bytes()
    manifest = json.loads((ROOT / "assets/brand-manifest.json").read_text())
    assert manifest["beacon_identity"] == "open-frame-02"
    for item in manifest["active_outputs"]:
        if "beacon" in item["path"] or "beacon" in item["role"]:
            assert hashlib.sha256((ROOT / item["path"]).read_bytes()).hexdigest() == item["sha256"], item["path"]


def test_mobile_and_embedded_marks_use_the_same_geometry():
    mark = ET.fromstring((MASTERS / "beacon-tools-mark-mono.svg").read_bytes())
    frame = mark.find("{http://www.w3.org/2000/svg}path").attrib["d"]
    mobile = (ROOT / "mobile/src/theme/beaconBrand.ts").read_text()
    assert json.dumps(frame) in mobile
    for name in ("relay/admin/admin.html", "relay/main.py", "src/localflight/ui/templates/admin.html"):
        source = (ROOT / name).read_text(encoding="utf-8")
        assert f'd="{frame}"' in source, name


def test_standalone_relay_has_matching_light_and_dark_images():
    source = (ROOT / "relay/public/index.html").read_text(encoding="utf-8")
    picture = re.search(r'<picture class="beacon-picture">(.*?)</picture>', source, re.S).group(1)
    assert '(prefers-color-scheme: dark)' in picture
    encoded = re.findall(r'data:image/png;base64,([^" ]+)', picture)
    assert len(encoded) == 2
    for payload, filename in zip(encoded, ("beacon-tools-mark-dark-96.png", "beacon-tools-mark-96.png")):
        assert base64.b64decode(payload) == (ROOT / "site/public/assets" / filename).read_bytes()
