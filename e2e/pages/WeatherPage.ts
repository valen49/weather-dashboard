import { Page, Locator } from '@playwright/test';

export class WeatherPage {
  readonly page: Page;
  readonly title: Locator;
  readonly weatherCard: Locator;
  readonly temperature: Locator;
  readonly windSpeed: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    this.title = page.locator('[data-testid="app-title"]');
    this.weatherCard = page.locator('[data-testid="weather-card"]');
    this.temperature = page.locator('[data-testid="temperature"]');
    this.windSpeed = page.locator('[data-testid="wind-speed"]');
    this.errorMessage = page.locator('[data-testid="error-message"]');
  }

  async goto() {
    await this.page.goto('/');
  }
}