# Branding coverage

Beacon Tools uses the approved **Open Frame** identity. Local Flight keeps its
product icon, display styles, data typography, native controls, and semantic
status colors. This inventory covers the full branding candidate, including the
earlier positioning and interface refresh. See [the brand guide](brand-guide.md).

## Public website

Every maintained page receives the shared studio identity, light/dark palette,
header, footer, focus treatment, metadata, and favicon where its layout permits.
The separate access-management layout keeps its restricted navigation.

| Page | Implementation and content review | Verification |
| --- | --- | --- |
| Homepage `/` | Approved studio hero and artwork, featured product, principles, attribution; retained anchors and paid-service explanation. | Responsive renders, accessibility and navigation contracts. |
| Local Flight `/local-flight/` | Equal BYOK, VATSIM and optional paid Relay choices; retained provider limits and downloads. | Responsive renders, data-choice and download contracts. |
| Mobile `/local-flight/mobile/` | Studio identity around Companion/Standalone explanation and store availability. | Responsive renders and store-link state tests. |
| Relay Access `/local-flight/relay-access/` | Studio identity around existing price, renewal, eligibility and purchase disclosures. | Responsive renders and checkout-state tests. |
| Connections `/network/` | All existing data paths and encryption explanations retained. | Responsive renders, content and link contracts. |
| Support `/support/` | Existing form fields, contact details and consent unchanged. | Responsive renders and form-submission fixtures. |
| Status `/status/` | Existing service status and unavailable/cached behavior retained. | Responsive renders and Worker status contracts. |
| Privacy `/privacy/` | Policy source unchanged. | Exact baseline comparison, responsive renders and accessibility. |
| Privacy choices `/privacy/choices/` | Policy controls and consent source unchanged. | Exact baseline comparison and form tests. |
| Legal / operator `/legal/` | Operator identity, addresses, contacts and disclosures unchanged. | Exact baseline comparison and responsive renders. |
| Service terms `/local-flight/relay-access/terms/` | Terms, prices, renewal and entitlement source unchanged. | Exact baseline comparison and responsive renders. |
| Purchase result `/local-flight/relay-access/success/` | Receipt, retry, one-time reveal and destination behavior unchanged. | Success, pending and error fixtures; responsive renders. |
| Access management `/local-flight/relay-access/manage/` | Separate branded layout; recovery, confirmation and device-change controls unchanged. | Fragment confirmation, recovery and access-management fixtures. |
| 404 `/404.html` | Open Frame header/footer around existing recovery actions. | Actual missing-route status, links, responsive renders and accessibility. |

## Applications and independent pages

| Surface | Implementation and content review | Verification |
| --- | --- | --- |
| Standalone Relay landing | Canonical embedded light/dark marks; approved palette and typography; all accepted layout content and destinations retained. | Direct standalone renders, production CSP, asset-byte, accessibility and link checks. |
| Separate Relay administration | Studio mark and palette; access boundaries and action scripts retained. | Isolated offline render; authenticated route and redaction regression tests. |
| Relay signed-out page | Studio signature and light/dark styling around the existing sign-in action and cache disclosure. | Isolated rendering and route regression tests. |
| Local browser administration | Compact canonical studio signature; original settings and actions retained. | Template rendering and local API regression suite. |
| Local browser setup | Earlier copy-catalog and shared visual refresh retained; provider choices unchanged. | Setup wizard checks, compact rendering and setup contracts. |
| Local browser splash | Earlier launch catalog and shared visual refresh retained. | Template rendering and launch contracts. |
| Local browser boards | Earlier shared visual refresh; Local Flight identity and board skins retained. | Rendered long rows, codeshares, empty/stale states and FIDS regression suite. |
| Local browser radar | Earlier shared visual refresh; selection and dismissal retained. | Rendered layouts and radar regression suite. |
| Local browser history | Earlier shared visual refresh and existing movement semantics retained. | Rendered layouts and history regression suite. |
| Local browser Matrix | Earlier shared visual refresh; display contract retained. | Rendered layouts and Matrix regression suite. |
| Local browser display/settings | Earlier shared visual refresh; all settings identifiers and controls retained. | Rendered layouts and settings regression suite. |
| Local browser logs/feedback/requests | Earlier shared visual refresh; sanitization and user-triggered submission unchanged. | Rendered layouts and API/privacy regression suite. |
| Local browser documentation | Shared viewer refresh and updated studio attribution in public documentation. | Template and bundled-document contracts. |
| Native desktop shell/footer | Canonical outlined studio lockup switches with appearance; existing link destinations retained. | Actual Qt light/dark footer renders and theme-switch/link regression test. |
| Native setup, display, boards, radar, history, Matrix | Earlier stylesheet and QApplication palette refresh retained; Local Flight identity unchanged. | Native regression suite; physical platform checks remain release gates. |
| Native settings, administration, requests, logs, feedback, documentation | Earlier shared palette and typography retained. | Native regression suite; physical platform checks remain release gates. |
| Mobile launch | Canonical studio mark and readable DM Sans attribution. | Type, launch, accessibility and source-geometry contracts. |
| Mobile widget preview | Canonical studio watermark; actual widget data/refresh behavior unchanged. | Widget contracts and canonical-geometry check. |
| Mobile help/about | Compact studio mark with existing help and legal links. | Type and accessibility checks. |
| Other mobile screens and native widgets | Earlier semantic palette/copy refresh retained; product icons, application identifiers and native widget contracts unchanged. | Full mobile verification on clean generated projects; physical checks pending. |
| Branded email | Readable studio wordmark and approved light palette; all transaction information and destinations retained. | Plain-text/HTML parity, escaping, delivery and recovery tests; no live emails sent. |
| Social cards | New studio artwork and consistent product maker signature. | Actual 1200×630 renders reviewed. |
| Current brand gallery and widget concept | Open Frame replaces the old studio mark; Local Flight artwork and existing gallery URLs retained. | Rendered assets and hash contracts. |
| Store descriptions and product previews | Earlier positioning updates retained; historical screenshots remain identifiable as earlier appearance. | Store metadata contracts; new native/store captures require their matching platforms. |

## Preservation and release gates

The baseline comparison covers 12 protected content groups, including the
legal/operator and privacy pages, service terms, support forms, safety notice,
existing site catalog, and all website action scripts. Existing URLs, redirects,
anchors, release facts, availability, consent, subscription, recovery, provider
timers, APIs and application identifiers are retained.

Clean-checkout CI is required before merging the candidate. The release-artifact
workflow requires the accepted current main commit; rebuild affected packages
from that commit before distributing them. Signing/notarization, physical
Windows/macOS/Linux/Pi/Matrix walkthroughs, mobile devices/widgets, store
processing, real-provider and Companion/Standalone checks remain release gates.
The review captures use isolated fixtures and do not certify those platforms.
