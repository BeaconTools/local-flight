import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import fs from "node:fs";
import path from "node:path";

test("studio and product introductions explain their distinct roles", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { level: 1 })).toHaveText("Complex data,made useful.");
  await expect(page.locator("[data-clock]")).toHaveCount(0);
  const preview = page.locator("#products .split-story-media img");
  await expect(preview).toBeVisible();
  expect((await preview.boundingBox())?.width).toBeGreaterThan(240);
  await page.goto("/local-flight/");
  const choices = page.locator("#flight-data .data-path-table article");
  await expect(choices).toHaveCount(3);
  await expect(choices.nth(0)).toContainText("Bring Your Own Keys (BYOK)");
  await expect(choices.nth(1)).toContainText("VATSIM");
  await expect(choices.nth(2)).toContainText("Beacon Relay");
  await expect(page.locator(".data-path-card--paid")).toHaveCount(0);
  await expect(page.locator("#flight-data")).toContainText("Provider charges, coverage, and refresh limits apply.");
  await expect(page.locator("#flight-data")).toContainText("Mobile Standalone uses VATSIM or Beacon Relay.");
});

test("404 keeps useful recovery links and studio branding", async ({ page }) => {
  const response = await page.goto("/missing-brand-review-page/");
  expect(response?.status()).toBe(404);
  await expect(page.getByRole("link", { name: "Go to Beacon Tools" })).toHaveAttribute("href", "/");
  await expect(page.getByRole("link", { name: "Get help", exact: true })).toHaveAttribute("href", "/support/");
  await expect(page.locator("[data-clock]")).toHaveCount(0);
});

test("Open Frame follows appearance across shared and private layouts", async ({ page }) => {
  for (const route of ["/", "/404.html", "/privacy/", "/local-flight/relay-access/manage/"]) {
    await page.goto(route);
    const mark = page.locator(".site-brand .beacon-mark, .management-brand .beacon-mark");
    await expect(mark).toBeVisible();
    await expect(mark).toHaveAttribute("viewBox", "0 0 64 64");
    for (const theme of ["light", "dark"]) {
      await page.evaluate(value => document.documentElement.dataset.theme = value, theme);
      await expect(mark).toHaveCSS("color", theme === "light" ? "rgb(49, 91, 214)" : "rgb(165, 189, 255)");
      if (!route.includes("/manage/")) {
        const footer = page.locator(`.beacon-lockup--${theme}`);
        await expect(footer).toBeVisible();
        await expect.poll(() => footer.evaluate((image: HTMLImageElement) => image.complete && image.naturalWidth > 0)).toBe(true);
        await expect(page.locator(`.beacon-lockup--${theme === "light" ? "dark" : "light"}`)).toBeHidden();
      }
    }
  }
});

test("brand introductions remain usable in forced colors", async ({ page }) => {
  await page.emulateMedia({ forcedColors: "active" });
  for (const route of ["/", "/local-flight/", "/404.html"]) {
    await page.goto(route);
    await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
    await page.keyboard.press("Tab");
    await expect(page.getByRole("link", { name: "Skip to main content" })).toBeFocused();
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
  }
});

test("standalone relay landing keeps disclosures and accessible styling", async ({ page }) => {
  const file = path.resolve("../relay/public/index.html");
  await page.route("https://relay.example.test/", route => route.fulfill({
    contentType: "text/html",
    headers: { "Content-Security-Policy": "default-src 'none'; img-src data:; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'" },
    body: fs.readFileSync(file, "utf8"),
  }));
  await page.goto("https://relay.example.test/");
  const logo = page.locator(".brand-mark");
  const expectedLogo = fs.readFileSync(path.resolve("public/assets/beacon-tools-mark-96.png")).toString("base64");
  await expect(logo).toHaveAttribute("src", `data:image/png;base64,${expectedLogo}`);
  await expect.poll(() => logo.evaluate((image: HTMLImageElement) => image.naturalWidth)).toBe(96);
  await expect(page.getByRole("heading", { level: 1 })).toHaveText("Your flight board, with hosted data.");
  await expect(page.locator("body")).toContainText("Bring Your Own Keys and VATSIM remain available without Relay Access.");
  await expect(page.locator("body")).toContainText("For display and hobby use only.");
  await expect(page.locator("a[href*='/admin']")).toHaveCount(0);
  expect((await new AxeBuilder({ page }).analyze()).violations).toEqual([]);
});
