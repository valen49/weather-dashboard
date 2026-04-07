import { test, expect } from '@playwright/test';
import { WeatherPage } from '../pages/WeatherPage';

test.describe('Weather Dashboard', () => {
  test('should display the app title', async ({ page }) => {
    const weatherPage = new WeatherPage(page);
    await weatherPage.goto();
    await expect(weatherPage.title).toBeVisible();
    await expect(weatherPage.title).toHaveText('Weather Dashboard');
  });

  test('should display weather card with data', async ({ page }) => {
    const weatherPage = new WeatherPage(page);
    await weatherPage.goto();
    await expect(weatherPage.weatherCard).toBeVisible();
    await expect(weatherPage.temperature).toBeVisible();
    await expect(weatherPage.windSpeed).toBeVisible();
  });

  test('should display temperature with celsius unit', async ({ page }) => {
    const weatherPage = new WeatherPage(page);
    await weatherPage.goto();
    const tempText = await weatherPage.temperature.textContent();
    expect(tempText).toContain('°C');
  });
});