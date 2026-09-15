import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import fs from "node:fs";
import path from "node:path";

test("studio and product introductions explain their distinct roles", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { level: 1 })).toHaveText("Complex data,made useful.");
  await expect(page.locator("[data-clock]")).toHaveCount(0);
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
  await page.goto("/404.html");
  await expect(page.getByRole("link", { name: "Go to Beacon Tools" })).toHaveAttribute("href", "/");
  await expect(page.getByRole("link", { name: "Get help", exact: true })).toHaveAttribute("href", "/support/");
  await expect(page.locator("[data-clock]")).toHaveCount(0);
});

test("standalone relay landing keeps disclosures and accessible styling", async ({ page }) => {
  const file = path.resolve("../relay/public/index.html");
  await page.route("**/*", route => route.fulfill({status: 503, body: ""}));
  await page.setContent(fs.readFileSync(file, "utf8"));
  await expect(page.getByRole("heading", { level: 1 })).toHaveText("Your flight board, with hosted data.");
  await expect(page.locator("body")).toContainText("Bring Your Own Keys and VATSIM remain available without Relay Access.");
  await expect(page.locator("body")).toContainText("For display and hobby use only.");
  await expect(page.locator("a[href*='/admin']")).toHaveCount(0);
  expect((await new AxeBuilder({ page }).analyze()).violations).toEqual([]);
});
