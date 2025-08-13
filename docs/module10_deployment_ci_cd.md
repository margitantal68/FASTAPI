---
marp: true
theme: gaia
author: Margit ANTAL
class:
    - lead 
    - invert
paginate: true
---
# Module 10: Deployment & CI/CD

## 🚀 Overview
- **Dockerizing** a FastAPI app
- Managing secrets with `.env`
- Deploying to **Render**, **Railway**, or **AWS**
- Intro to **CI/CD** with GitHub Actions

---

## 🐳 Dockerizing a FastAPI App
1. Create a `Dockerfile`
2. Use an official Python base image
3. Install dependencies
4. Run with **Uvicorn**
5. Test locally before deployment

---

## 🔑 Using .env & Environment Variables
- Store secrets like:
  - Database URLs
  - API keys
  - Debug flags
- Use **python-dotenv** or **Pydantic Settings**
- Never commit `.env` to GitHub

---

## ☁️ Deployment Options
-  **Render**
    - Simple, free tier
    - Auto deploy from GitHub

- **Railway**
    - Great for quick prototypes
    - Easy database integration

- **AWS**
    - Full flexibility
    - Options: EC2, Elastic Beanstalk, ECS, Lambda

---

## ⚙️ Introduction to CI/CD
- **Continuous Integration (CI)**
  - Automated tests
  - Linting & type checks
- **Continuous Deployment (CD)**
  - Auto-deploy after successful CI
- Tools: **GitHub Actions**, GitLab CI, CircleCI

---

## 💡 GitHub Actions Workflow Example
```yaml
name: CI/CD
on:
  push:
    branches: [ main ]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: pytest
```
---

## 🎯 Remember

- Containerize with Docker for portability
- Manage secrets via .env
- Choose a hosting platform that fits your needs
- Automate testing & deployment with CI/CD
