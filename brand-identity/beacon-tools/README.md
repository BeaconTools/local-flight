# Beacon Tools brand identity

The approved **Open Frame 02** identity, ready for websites, apps, print layouts
and branded communications. Open [the visual index](index.html) to choose an asset.

## Choose a file

| Folder | Contents / use |
| --- | --- |
| `svg/marks` | Standalone Open Frame symbol. Scales to any size. |
| `svg/lockups` | Symbol and outlined “beacon tools” lettering together. |
| `svg/lettering` | Outlined lettering alone; no font installation needed. |
| `png/transparent/marks` | Cobalt, mist, ink and paper marks at 16, 24, 32, 48, 64, 96, 128, 180, 256, 512 and 1024 px. |
| `png/transparent/lockups` | Full logo at 320, 640 and 1280 px wide. |
| `png/transparent/lettering` | Lettering at 320, 640 and 1280 px wide. |
| `png/on-light`, `png/on-dark` | Finished exports with opaque brand backgrounds. |
| `icons` | Multi-size favicon, 32 px PNG favicon and 180 px touch icon. |
| `licenses` | DM Sans lettering license. |
| `manifest.json` | Logical source references, checksums, sizes and transparency. |

`light` means **for a light background**: cobalt symbol and dark ink lettering.
`dark` means **for a dark background**: mist symbol and paper lettering.
`ink` and `paper` are single-color alternatives. `mono` is an SVG-only
`currentColor` mark for application interfaces. All SVGs and all files under
`png/transparent` have no background; empty space is transparent, not white.

## Identity rules

- Positioning: **Complex data, made useful.**
- Description: An independent software studio turning complex data and APIs
  into approachable applications.
- Attribution: **Built by Philipp.**
- Lettering: lowercase DM Sans, weight 600, optical size 27, tracking −0.035em.
- Keep the geometric gap and detached square. Do not stretch or add shadows,
  gradients, an outline, or a new container to the logo itself.
- Leave at least 8 units of clear space around the 64-unit symbol.
- Use SVG when possible. Small PNGs are for small interface placements;
  use larger exports when placing raster assets at higher pixel density.

| Role | Light appearance | Dark appearance |
| --- | --- | --- |
| Canvas | `#F7F8F3` | `#17201E` |
| Text | `#202B29` | `#F3F5ED` |
| Muted text | `#58655F` | `#ABB9AE` |
| Brand/action color | `#315BD6` | `#A5BDFF` |

Local Flight retains its own product identity. This folder contains Beacon Tools
studio artwork only. See [the full brand guide](../../docs/brand-guide.md).

## Source and regeneration

Canonical application masters remain in `assets/beacon-tools`. This is the
portable export kit; do not edit its generated artwork by hand. From the
repository root, run:

```sh
python scripts/sync_beacon_brand.py
python scripts/export_beacon_identity.py
python scripts/export_beacon_identity.py --check
```

The export command refreshes the kit without changing application assets or
deleting files. Existing public asset URLs remain supported. Retired design
studies and temporary review files are cleaned up after final visual approval;
historical product releases and current legal/privacy records remain intact.
