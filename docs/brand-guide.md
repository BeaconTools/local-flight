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

Keep the existing logos, icons, names, DM Sans interface face, Space Mono data
face, and Audiowide brand face. Use calm neutral surfaces, blue actions,
restrained cyan highlights, subtle borders, and clear semantic status colors.

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

Social cards use the existing Beacon Tools mark and bundled fonts. From `site`,
run `node scripts/render-social.mjs` after changing the public positioning catalog,
then review both generated cards before committing them.

## Content protection and coverage

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
