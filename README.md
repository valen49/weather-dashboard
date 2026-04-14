# 🌤️ Weather Dashboard

A modern, containerized Flask web application that displays real-time weather data using the Open-Meteo API. This project demonstrates best practices in DevOps, CI/CD, and cloud-native development.

## ✨ Features

- 🔍 **City Search**: Real-time weather lookup by city name
- 🌡️ **Current Conditions**: Temperature, wind speed, and weather status
- 📅 **7-Day Forecast**: Extended weather predictions
- 🔄 **Unit Toggle**: Switch between Celsius and Fahrenheit
- ⚖️ **City Comparison**: Compare weather between two locations
- 🌦️ **Weather Icons**: Dynamic icons based on WMO weather codes
- 📱 **Responsive Design**: Mobile-friendly interface
- 🐳 **Containerized**: Docker-ready for easy deployment
- ☸️ **Kubernetes Ready**: Production deployment manifests included

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   External API  │
│   (HTML/CSS/JS) │◄──►│   Flask App     │◄──►│   Open-Meteo     │
│                 │    │   Python 3.11   │    │   (Free API)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   Database      │
                       │   (None - API   │
                       │    only)        │
                       └─────────────────┘
```

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | Python 3.11 + Flask | Web framework |
| **Frontend** | HTML5 + CSS3 + JavaScript | User interface |
| **API** | Open-Meteo | Weather data (free, no API key) |
| **Testing** | pytest + Playwright | Unit & E2E testing |
| **CI/CD** | Jenkins | Automated pipelines |
| **Container** | Docker | Application packaging |
| **Orchestration** | Kubernetes | Production deployment |
| **Version Control** | Git + GitHub | Code management |

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+ (for local development)
- Node.js 20+ (for E2E tests)

### Local Development

```bash
# Clone repository
git clone https://github.com/valen49/weather-dashboard.git
cd weather-dashboard

# Start with Docker Compose (recommended)
docker-compose up --build

# Or run locally
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
pip install -r requirements.txt -r requirements-dev.txt
python run.py
```

Visit `http://localhost:5000` in your browser.

### Testing

```bash
# Unit tests
pytest tests/ -v --cov=app

# E2E tests
npx playwright install
npx playwright test --headed  # Visual mode
npx playwright test           # Headless mode
```

### Code Quality

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Format code
black app/ tests/
isort app/ tests/

# Lint code
flake8 app/ tests/
mypy app/

# Run all checks
pre-commit run --all-files
```

## 🐳 Docker Deployment

### Build Images
```bash
# Application image
docker build -t weather-dashboard:latest .

# E2E testing image
docker build -f Dockerfile.e2e -t weather-dashboard-e2e:latest .
```

### Run Locally
```bash
# Start application
docker run -p 5000:5000 weather-dashboard:latest

# Run E2E tests
docker run --network host weather-dashboard-e2e:latest
```

## ☸️ Kubernetes Deployment

### Prerequisites
- Kubernetes cluster (local: minikube/kind, cloud: EKS/GKE/AKS)
- kubectl configured

### Deploy
```bash
# Apply manifests
kubectl apply -f k8s-deployment.yaml
kubectl apply -f k8s-service.yaml

# Check deployment
kubectl get pods
kubectl get services

# View logs
kubectl logs -l app=weather-dashboard
```

### Access Application
```bash
# Port forward (local access)
kubectl port-forward svc/weather-dashboard 5000:5000

# Or get external IP
kubectl get svc weather-dashboard
```

## 🔄 CI/CD Pipeline

### Jenkins Setup
The project includes a comprehensive Jenkins pipeline (`Jenkinsfile`) with:

- **Parallel Builds**: Unit tests + Docker image builds run simultaneously
- **Automated Testing**: pytest unit tests + Playwright E2E tests
- **Container Security**: Images built with best practices
- **Kubernetes Deploy**: Automatic deployment to K8s cluster
- **Health Checks**: Post-deployment verification

### Pipeline Stages
1. **Checkout**: Git clone and workspace setup
2. **Parallel Execution**:
   - Unit Tests (Python + pytest)
   - Build App Image (Docker)
   - Build E2E Image (Docker)
3. **E2E Tests**: Playwright tests against deployed app
4. **Validation**: Kubernetes manifest checks
5. **Deploy**: Rolling update to production
6. **Health Check**: Application availability verification

### Jenkins Configuration
1. Install required plugins: Docker, Kubernetes
2. Configure credentials for Docker registry and K8s cluster
3. Set environment variables in Jenkins
4. Trigger builds on Git push or manually

## 📁 Project Structure

```
weather-dashboard/
├── app/                          # Flask application
│   ├── __init__.py              # App factory
│   ├── routes.py                # API endpoints
│   ├── services.py              # Open-Meteo integration
│   └── templates/
│       └── index.html           # Frontend UI
├── tests/                        # Unit tests
│   ├── test_app.py
│   ├── test_routes.py
│   └── test_services.py
├── e2e/                          # End-to-end tests
│   ├── locators/
│   │   └── weather.locators.ts
│   ├── pages/
│   │   └── WeatherPage.ts
│   └── tests/
│       └── weather.spec.ts
├── k8s-*.yaml                    # Kubernetes manifests
├── Dockerfile                    # App container
├── Dockerfile.e2e                # E2E test container
├── docker-compose.yml            # Local development
├── Jenkinsfile                   # CI/CD pipeline
├── playwright.config.ts          # E2E test config
├── requirements*.txt             # Python dependencies
└── README.md                     # This file
```

## 🔧 Development

### Code Quality
```bash
# Lint Python code
pip install flake8 black
flake8 app/ tests/
black app/ tests/

# Format code
black --check --diff app/ tests/
```

### Adding Features
1. Backend changes in `app/`
2. Frontend changes in `app/templates/`
3. Tests in `tests/` or `e2e/tests/`
4. Update Docker images if dependencies change
5. Test pipeline locally before pushing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📊 Monitoring & Observability

- **Health Checks**: Built-in `/health` endpoint
- **Logs**: Application logs available via `kubectl logs`
- **Metrics**: Basic request counting (expandable)
- **Alerts**: Pipeline failure notifications

## 🔒 Security

- Container images use minimal base images
- No sensitive data in codebase
- Dependencies regularly updated
- Security scanning in CI pipeline

## 📈 Roadmap

- [ ] Add weather alerts/notifications
- [ ] Implement user preferences
- [ ] Add historical weather data
- [ ] Mobile app companion
- [ ] Multi-language support

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Open-Meteo](https://open-meteo.com/) for the excellent free weather API
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [Playwright](https://playwright.dev/) for E2E testing
- [Docker](https://www.docker.com/) for containerization

---

**Built with ❤️ for learning DevOps and cloud-native development**
