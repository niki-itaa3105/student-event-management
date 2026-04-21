# 🎓 Student Event Management System

A full-stack DevOps project built with **Flask + MySQL + Docker + GitHub Actions CI/CD**.

---

## 📁 Project Structure

```
student-event-management/
├── app/
│   ├── app.py                  # Flask application
│   ├── requirements.txt        # Python dependencies
│   ├── Dockerfile              # Docker image for Flask app
│   └── templates/              # HTML pages
│       ├── base.html
│       ├── home.html
│       ├── register.html
│       ├── login.html
│       ├── events.html
│       └── my_events.html
├── database/
│   └── init.sql                # DB schema + sample data
├── .github/
│   └── workflows/
│       └── ci-cd.yml           # GitHub Actions CI/CD pipeline
├── docker-compose.yml          # Runs Flask + MySQL together
├── .env                        # Environment variables
└── README.md
```

---

## 🚀 How to Run

### Prerequisites
- Docker Desktop installed and running
- Git installed

### Steps

```bash
# 1. Clone the project
git clone <your-repo-url>
cd student-event-management

# 2. Start everything with Docker Compose
docker compose up --build

# 3. Open in browser
http://localhost:5000
```

---

## ✅ Features

| Feature | Description |
|---|---|
| Register | Student can create an account |
| Login / Logout | Secure session-based auth |
| Browse Events | View all upcoming college events |
| Register for Event | One-click event registration |
| My Events | View your registered events |

---

## 🐳 DevOps Components

| File | Purpose |
|---|---|
| `Dockerfile` | Containerizes the Flask app |
| `docker-compose.yml` | Orchestrates Flask + MySQL containers |
| `.env` | Stores environment variables |
| `ci-cd.yml` | GitHub Actions: build → test → push → deploy |

---

## 🔐 GitHub Secrets Required

Add these in your repo → Settings → Secrets → Actions:

| Secret | Value |
|---|---|
| `DOCKER_USERNAME` | Your Docker Hub username |
| `DOCKER_PASSWORD` | Your Docker Hub password |
