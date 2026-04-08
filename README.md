markdown# 🌤️ Weather Dashboard

A Flask web application that displays real-time weather data using the Open-Meteo API. Built as part of a DevOps learning course.

## Features

- 🔍 Search weather by city name
- 🌡️ Current temperature, wind speed and weather conditions
- 📅 7-day weather forecast
- 🔄 Toggle between °C and °F
- ⚖️ Compare weather between two cities
- 🌦️ Weather icons based on WMO weather codes
- 📱 Responsive UI

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python / Flask |
| Weather API | Open-Meteo (free, no API key required) |
| Testing | pytest + Playwright |
| CI | GitHub Actions |
| CD | Jenkins (Docker agent) |
| Version Control | Git / GitHub |

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 20+

### Installation

```bash
# Clone the repository
git clone git@github.com:valen49/weather-dashboard.git
cd weather-dashboard

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
npm install
```

### Run the app

```bash
python run.py
```

Open `http://localhost:5000` in your browser.

## Running Tests

### Unit tests

```bash
pytest tests/ -v
```

### E2E tests

```bash
npx playwright test
```

## CI/CD Pipeline

### GitHub Actions
Runs automatically on every push to any branch:
- Unit tests with pytest
- E2E tests with Playwright (Chromium)

### Jenkins
Runs manually or triggered via GitHub Actions:
- Unit tests stage (Docker agent: `python:3.11`)
- E2E tests stage (Docker agent: `mcr.microsoft.com/playwright/python:v1.58.0-noble`)

## Project Structure
weather-dashboard/
├── app/
│   ├── init.py        # App factory
│   ├── routes.py          # Flask routes
│   ├── services.py        # Open-Meteo API integration
│   └── templates/
│       └── index.html     # Main UI
├── tests/
│   └── test_services.py   # Unit tests
├── e2e/
│   ├── locators/          # Page locators
│   ├── pages/             # Page Object Model
│   └── tests/             # E2E test specs
├── .github/
│   └── workflows/
│       └── ci.yml         # GitHub Actions workflow
├── Jenkinsfile            # Jenkins pipeline
└── requirements.txt

## License

MIT