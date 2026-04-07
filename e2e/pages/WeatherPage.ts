import { Page, Locator } from '@playwright/test';
import { WeatherLocators } from '../locators/weather.locators';

export class WeatherPage {
  readonly page: Page;
  readonly title: Locator;
  readonly weatherCard: Locator;
  readonly temperature: Locator;
  readonly windSpeed: Locator;
  readonly errorMessage: Locator;
  readonly cityInput: Locator;
  readonly searchButton: Locator;
  readonly locationName: Locator;
  readonly notFoundMessage: Locator;
  readonly forecastContainer: Locator;
  readonly forecastCards: Locator;

  constructor(page: Page) {
    this.page = page;
    this.title = page.locator(WeatherLocators.appTitle);
    this.weatherCard = page.locator(WeatherLocators.weatherCard);
    this.temperature = page.locator(WeatherLocators.temperature);
    this.windSpeed = page.locator(WeatherLocators.windSpeed);
    this.errorMessage = page.locator(WeatherLocators.errorMessage);
    this.cityInput = page.locator(WeatherLocators.cityInput);
    this.searchButton = page.locator(WeatherLocators.searchButton);
    this.locationName = page.locator(WeatherLocators.locationName);
    this.notFoundMessage = page.locator(WeatherLocators.notFoundMessage);
    this.forecastContainer = page.locator(WeatherLocators.forecastContainer);
    this.forecastCards = page.locator(WeatherLocators.forecastCard);
  }

  async goto() {
    await this.page.goto('/');
  }

  async searchCity(city: string) {
    await this.cityInput.fill(city);
    await this.searchButton.click();
  }
}