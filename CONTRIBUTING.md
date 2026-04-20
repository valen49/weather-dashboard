# Contributing to Weather Dashboard

## Branch naming

| Type | Pattern | Example |
|------|---------|---------|
| Feature | `feature/<short-description>` | `feature/unit-toggle` |
| Bug fix | `fix/<short-description>` | `fix/health-endpoint` |
| Chore / refactor | `chore/<short-description>` | `chore/update-deps` |

Never commit directly to `main`. All changes go through a PR.

## Commit messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add Celsius/Fahrenheit toggle
fix: return dynamic timestamp in /health
chore: update playwright to 1.44
```

Types: `feat`, `fix`, `refactor`, `test`, `chore`, `docs`.

## Workflow

1. Branch off `main`: `git checkout -b feature/my-feature`
2. Make changes and commit
3. Push: `git push origin feature/my-feature`
4. Open a PR against `main`
5. CI (GitHub Actions) must pass before merging
6. Squash and merge

## Running tests locally

```bash
# Unit tests
pip install -r requirements.txt -r requirements-dev.txt
pytest tests/ -v

# E2E tests
npm ci
npx playwright install chromium --with-deps
python run.py &
npx playwright test --project=chromium
```

## Code style

This project uses [Black](https://black.readthedocs.io/) and [isort](https://pycqa.github.io/isort/). Run before committing:

```bash
black app/ tests/
isort app/ tests/
```

Or install pre-commit hooks:

```bash
pip install pre-commit
pre-commit install
```
