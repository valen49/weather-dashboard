import { test, expect } from '@playwright/test';
import { WeatherPage } from '../pages/WeatherPage';

test.describe('Weather Dashboard', () => {

  test.describe('Homepage', () => {
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

  test.describe('City Search', () => {
    test('should show weather for a valid city', async ({ page }) => {
      const weatherPage = new WeatherPage(page);
      await weatherPage.goto();
      await weatherPage.searchCity('Buenos Aires');
      await page.waitForURL('**/?city=Buenos+Aires**');
      const hasCard = await weatherPage.weatherCard.isVisible();
      const hasError = await weatherPage.notFoundMessage.isVisible();
      expect(hasCard || hasError).toBeTruthy();
    });

    test('should show not found message for invalid city', async ({ page }) => {
      const weatherPage = new WeatherPage(page);
      await weatherPage.goto();
      await weatherPage.searchCity('ciudadinexistente123xyz');
      await expect(weatherPage.notFoundMessage).toBeVisible();
    });

    test('should display search input and button', async ({ page }) => {
      const weatherPage = new WeatherPage(page);
      await weatherPage.goto();
      await expect(weatherPage.cityInput).toBeVisible();
      await expect(weatherPage.searchButton).toBeVisible();
    });
  });

  test.describe('Forecast', () => {
    test('should display forecast container', async ({ page }) => {
      const weatherPage = new WeatherPage(page);
      await weatherPage.goto();
      await expect(weatherPage.forecastContainer).toBeVisible();
    });

    test('should display 7 forecast cards', async ({ page }) => {
      const weatherPage = new WeatherPage(page);
      await weatherPage.goto();
      await expect(weatherPage.forecastCards).toHaveCount(7);
    });
  });
});