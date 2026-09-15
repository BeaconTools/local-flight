/** Render typographic social cards with the existing logos and bundled fonts. */
import { chromium } from "@playwright/test";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { brand } from "../src/data/site.ts";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../public");
const browser = await chromium.launch();
try {
  const page = await browser.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
  await page.route("http://brand.test/**", async route => {
    const pathname = new URL(route.request().url()).pathname;
    const file = path.resolve(root, `.${pathname}`);
    if (!file.startsWith(`${root}${path.sep}`)) return route.abort();
    await route.fulfill({ body: await fs.readFile(file) });
  });
  for (const product of [false, true]) {
    const title = product ? brand.productTagline : brand.studioTagline;
    const description = product
      ? "Aviation data, brought together on your own screens."
      : brand.studioDescription;
    const footer = product ? "BYOK · VATSIM · Optional Beacon Relay" : brand.attribution;
    const logo = product ? "/assets/localflight-lockup.png" : "/assets/beacon-tools-mark-96.png";
    await page.setContent(`<!doctype html><html lang="en"><head><style>
      @font-face { font-family: 'DM Sans'; src: url('http://brand.test/assets/fonts/DMSans.ttf'); font-weight: 100 1000; }
      @font-face { font-family: 'Space Mono'; src: url('http://brand.test/assets/fonts/SpaceMono-Regular.ttf'); }
      * { box-sizing: border-box; } body { margin: 0; padding: 62px 72px; background: #10151b; color: #edf2f7; font-family: 'DM Sans', sans-serif; }
      header { display: flex; align-items: center; gap: 16px; font-size: 26px; font-weight: 650; }
      header img { width: ${product ? 210 : 52}px; height: 52px; object-fit: contain; }
      h1 { font-size: 80px; line-height: 1.06; letter-spacing: -.045em; max-width: 950px; margin: 50px 0 24px; }
      p { color: #a5b4c3; font-size: 27px; line-height: 1.45; max-width: 900px; margin: 0; }
      footer { display: flex; justify-content: space-between; position: absolute; bottom: 48px; left: 72px; right: 72px; padding-top: 23px; border-top: 1px solid #394957; color: #7ce7ff; font: 17px 'Space Mono', monospace; }
    </style></head><body><header><img src="http://brand.test${logo}" alt="">${product ? "by Beacon Tools" : "Beacon Tools"}</header><h1>${title}</h1><p>${description}</p><footer><span>${footer}</span><span>beacontools.cc${product ? "/local-flight" : ""}</span></footer></body></html>`);
    await page.evaluate(async () => { await document.fonts.ready; await Promise.all([...document.images].map(i => i.decode())); });
    await page.screenshot({ path: path.join(root, "assets", product ? "localflight-social.png" : "beacon-tools-social.png") });
  }
} finally {
  await browser.close();
}
