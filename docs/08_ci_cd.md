# CI/CD Setup with GitHub Actions

This guide explains how to automate testing and deployment using GitHub Actions.

## 1. Setting Up GitHub Actions
Create a workflow file in `.github/workflows/ci.yml`:

```yaml
name: CI/CD Pipeline

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      
      - name: Run tests
        run: pytest

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to Render
        run: |
          curl -X POST "$RENDER_DEPLOY_HOOK"
```

## 2. Adding Secrets to GitHub
1. Go to **GitHub Repository → Settings → Secrets and Variables**.
2. Add `RENDER_DEPLOY_HOOK` for Render auto-deployment.

## 3. Running Tests Locally
```sh
pytest
```

## 4. Auto Deployment
- Code is tested and deployed when pushed to `main`.
- Modify the script for **Docker-based deployment** if needed.

Your CI/CD pipeline is now automated! 🚀

