/** Render current studio/product cards from canonical artwork and bundled fonts. */
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
    const contentType = file.endsWith(".svg") ? "image/svg+xml" : file.endsWith(".ttf") ? "font/ttf" : "image/png";
    await route.fulfill({ contentType, body: await fs.readFile(file) });
  });
  for (const product of [false, true]) {
    const title = product ? brand.productTagline : brand.studioTagline;
    const description = product
      ? "Aviation data, brought together on your own screens."
      : brand.studioDescription;
    const footer = product ? "BYOK · VATSIM · Optional Beacon Relay" : brand.attribution;
    const logo = product ? "/assets/localflight-lockup.png" : "/assets/beacon-tools-lockup-paper.svg";
    await page.setContent(`<!doctype html><html lang="en"><head><style>
      @font-face { font-family: 'DM Sans'; src: url('http://brand.test/assets/fonts/DMSans.ttf'); font-weight: 100 1000; }
      @font-face { font-family: 'Space Mono'; src: url('http://brand.test/assets/fonts/SpaceMono-Regular.ttf'); }
      * { box-sizing: border-box; } body { margin: 0; padding: 62px 72px; background: ${product ? "#17201e" : "#315bd6"}; color: #f3f5ed; font-family: 'DM Sans', sans-serif; }
      header { display: flex; align-items: center; gap: 16px; font-size: 26px; font-weight: 650; }
      header img { width: ${product ? 210 : 265}px; height: 52px; object-fit: contain; }
      header .studio-signature { width: 180px; height: 36px; }
      h1 { position: relative; font-weight: 500; font-size: 80px; line-height: 1.06; letter-spacing: -.045em; max-width: 950px; margin: 50px 0 24px; }
      p { position: relative; color: ${product ? "#abb9ae" : "#f3f5ed"}; font-size: 27px; line-height: 1.45; max-width: 900px; margin: 0; }
      footer { display: flex; justify-content: space-between; position: absolute; bottom: 48px; left: 72px; right: 72px; padding-top: 23px; border-top: 1px solid ${product ? "#47594b" : "#a5bdff"}; color: ${product ? "#a5bdff" : "#f3f5ed"}; font: 17px 'DM Sans', sans-serif; }
      .graphic { position: absolute; right: -70px; bottom: -85px; width: 400px; opacity: .10; }
    </style></head><body>${product ? "" : '<img class="graphic" src="http://brand.test/assets/beacon-tools-mark-paper.svg" alt="">'}<header><img src="http://brand.test${logo}" alt="">${product ? 'by <img class="studio-signature" src="http://brand.test/assets/beacon-tools-lockup-dark.svg" alt="Beacon Tools">' : ""}</header><h1>${title}</h1><p>${description}</p><footer><span>${footer}</span><span>beacontools.cc${product ? "/local-flight" : ""}</span></footer></body></html>`);
    await page.evaluate(async () => { await document.fonts.ready; await Promise.all([...document.images].map(i => i.decode())); });
    await page.screenshot({ path: path.join(root, "assets", product ? "localflight-social.png" : "beacon-tools-social.png") });
  }
} finally {
  await browser.close();
}
