# Beacon Tools and Local Flight

## Positioning

**Beacon Tools — Complex data, made useful.**

An independent software studio turning complex data and APIs into approachable
applications. Use the studio voice, with a small **Built by Philipp** attribution.
Local Flight is the featured product. Describe actual products and capabilities.

**Local Flight — Your flight board. Your way.**

Turn aviation data into arrivals and departures boards, nearby-aircraft radar,
weather, and movement history. Choose your data source and display it across
your own devices.

Write for aviation enthusiasts first. Explain APIs as connections to supported
aviation-data providers. Show the value of combining sources, grouping
codeshares, retaining cached boards, recording movements, and serving screens.

## Data choices

Present three equally weighted choices: **Bring Your Own Keys (BYOK)**,
**VATSIM**, and optional paid **Beacon Relay**. Provider charges, licensing,
coverage, and refresh limits still apply to BYOK. Supported schedule providers
include AeroDataBox and AviationStack; aircraft-position sources include ADS-B
Exchange and OpenSky. Avoid promising arbitrary API compatibility.

Desktop BYOK can feed mobile Companion through the host. Mobile Standalone
uses VATSIM or real-flight Relay Access; it does not accept desktop provider
keys. Retain all existing subscription, founder-access, consent, freshness,
availability, and informational-use qualifications.

## Visual language

Beacon Tools uses **Open Frame**, the approved studio mark and lowercase
wordmark. Canonical, font-independent SVG artwork lives in `assets/beacon-tools/`.
The mark has a 64-unit canvas, a 48-unit silhouette, 12-unit frame thickness,
and 8-unit openings. Soft outer and inner corners retain the geometric structure.
Keep the detached square aligned and preserve the supplied proportions.

Use the full lockup where space allows, and the mark with a readable name or
accessible label in compact placements. A 16px mark canvas is the minimum;
24px or larger is preferred. Allow at least one frame thickness of external
clear space. Decorative marks are hidden from assistive technology.

The studio wordmark uses DM Sans at weight 600, optical-size axis 27, and
−0.035em tracking. Exported lockups contain outlines, so they do not depend on
font availability. Use the light artwork on light surfaces, the dark artwork
on dark surfaces, or the one-color ink/paper variants. Do not add a background
plate, recreate the mark in CSS, distort it, apply color filters, or add glow.

| Studio role | Light | Dark |
| --- | --- | --- |
| Canvas | `#F7F8F3` | `#17201E` |
| Primary text | `#202B29` | `#F3F5ED` |
| Secondary text | `#58655F` | `#ABB9AE` |
| Brand / action | `#315BD6` | `#A5BDFF` |
| Text on action | `#FFFFFF` | `#182849` |

Use generous spacing, restrained borders, 7px action corners, and 8–12px content
frames. Carry the frame into layouts and imagery sparingly. The homepage leads
with the studio, its promise, and a quiet graphic, followed by Local Flight.
Branded email keeps a readable text wordmark when images and custom fonts are
unavailable. Customer transaction wording remains identical across alternatives.

Local Flight retains its product logos, app icons, DM Sans interface face,
Space Mono data face, and Audiowide short product treatments. Keep the product's
calm neutral surfaces, blue actions, restrained cyan highlights, and clear
semantic status colors. Beacon Tools is a compact maker signature in the app.

Standard dark surfaces use #10151b, #171e26, and #1e2731; light surfaces use
#f5f7f9, #ffffff, and #edf1f5. Primary text uses #edf2f7 or #18232e; secondary
text uses #a5b4c3 or #506174. Keep special board skins and high-contrast choices.
Use existing spacing scales and platform controls. Preserve dense display
layouts while improving hierarchy and focus visibility.

The studio homepage leads with the studio promise and a featured product.
Airport instruments and clocks belong to Local Flight contexts. Use real
application captures with accurate labels; illustrative previews are labeled.

The browser board captures in `site/src/assets/screens/shell/fids-browser-*.png`
show the refreshed interface with demonstration data. Older desktop and mobile
captures retain their original files and must not be described as showing a new
appearance. Refresh native store screenshots on their matching physical or
simulated platforms before the next store submission.

Run `python scripts/sync_beacon_brand.py` to synchronize studio SVGs, compatible
PNGs/favicons, mobile vector geometry, standalone marks, and the current brand
gallery. Run it with `--check` to verify canonical copies and recorded hashes.
This pipeline does not regenerate Local Flight product icons. The older full
brand pipeline defaults to the committed Beacon masters and runs the studio
sync after a full regeneration to refresh its additional consumers.

Social cards use Open Frame and bundled fonts. From `site`, run
`node scripts/render-social.mjs` after changing the positioning catalog or studio
artwork, then review both generated cards before committing them. Rebuild
affected packages and follow the existing release gates before publication.

## Content protection and coverage

The portable [Beacon Tools identity kit](../brand-identity/beacon-tools/README.md)
contains transparent size exports, light/dark variants, outlined lettering,
favicons and a visual index. Regenerate it with
`python scripts/export_beacon_identity.py` after synchronizing the canonical
studio masters. `--check` verifies source hashes, dimensions and transparency.

Legal, privacy, operator, terms, subscription, recovery, and consent information
is protected. Restyling must preserve its content, destinations, and behavior.
Preserve route addresses, redirects, download anchors, and release facts.
Historical release records remain historical.

Apply the brand to every maintained web surface, including independent relay
pages, error pages, access-management layouts, and local browser screens.
Keep administrative navigation separate from public navigation. Use shared
copy and theme sources wherever the platform already provides them.

App messages continue to explain the state, then the next step. Marketing
taglines belong in introductions and brand treatments, not repeated inside
operational messages, data rows, or transactional instructions.
