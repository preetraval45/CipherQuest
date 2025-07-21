# CipherQuest - Hack. Learn. Level Up

[![Build Status](https://github.com/preetraval45/CipherQuest/actions/workflows/ci.yml/badge.svg)](https://github.com/preetraval45/CipherQuest/actions)
[![Codecov Coverage](https://codecov.io/gh/preetraval45/CipherQuest/branch/main/graph/badge.svg)](https://codecov.io/gh/preetraval45/CipherQuest)
[![Docker Build](https://img.shields.io/docker/cloud/build/preetraval45/cipherquest-backend?label=Backend%20Docker)](https://hub.docker.com/r/preetraval45/cipherquest-backend)
[![Vercel Deploy](https://vercelbadge.vercel.app/api?app=cipherquest-frontend)](https://cipherquest-frontend.vercel.app/)
[![Heroku Deploy](https://img.shields.io/badge/dynamic/json?color=430098&label=Heroku%20API&query=%24.status&url=https%3A%2F%2Fapi.heroku.com%2Fapps%2F${{ secrets.HEROKU_APP_NAME }}&logo=heroku)](https://dashboard.heroku.com/apps)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A modern, cyberpunk-themed cybersecurity learning platform built with HTML, CSS, and JavaScript.

---

## 🛡️ Security Overview

CipherQuest is built with security as a top priority. The platform implements:
- **Comprehensive security headers** (CSP, HSTS, X-Frame-Options, etc.)
- **Strict environment variable management** (no hardcoded secrets)
- **Rate limiting and CORS controls**
- **Input validation and secure authentication**
- **Automated security validation tools**

See [SECURITY.md](SECURITY.md) for full details on security practices, headers, and compliance.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 14+
- Docker & Docker Compose (for full-stack deployment)
- Modern web browser (Chrome, Firefox, Safari, Edge)

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/cipherquest.git
cd cipherquest
```

### 2. Generate Secure Environment Variables
Use the provided script to generate a secure `.env` file:
```bash
python generate-secrets.py
```
- This will create `backend/.env` with strong random secrets and passwords.
- **Never commit `.env` files to version control!**

### 3. Review & Customize Environment Variables
- Edit `backend/.env` as needed (see [Environment Variables](#-environment-variables) below).
- For production, use unique, strong secrets and passwords.

### 4. Install Dependencies
```bash
# Backend
cd backend
pip install -r requirements.txt
cd ..

# Frontend
cd frontend
npm install
cd ..
```

### 5. Run Security Validation (Recommended)
Check your setup for common security issues:
```bash
python security-check.py
```
- This script checks for hardcoded secrets, missing environment variables, and security header configuration.

### 6. Start the Application
#### Local Development
- **Backend:**
  ```bash
  cd backend
  python run.py
  ```
- **Frontend:**
  ```bash
  cd frontend
  npm start
  ```
- Access at [http://localhost:3000](http://localhost:3000)

#### Docker Compose (Full Stack)
```bash
docker-compose up --build
```
- This will start the database, backend, and frontend with all secrets loaded from environment variables.

## 🧪 Running Tests

### Backend
```bash
cd backend
pytest
```

### Frontend
```bash
cd frontend
npm test
# or
yarn test
```

## 🐳 Docker Troubleshooting

- **Port Conflicts:**  
  Ensure ports 3000 (frontend), 5000 (backend), and 3307 (MySQL) are free.
- **Volume Permissions:**  
  On Linux/Mac, you may need to adjust permissions for `db_data` volume:
  ```bash
  sudo chown -R $USER:$USER ./db_data
  ```
- **Database Connection Issues:**  
  - Check that the `db` service is healthy (`docker ps`).
  - Ensure environment variables in `docker-compose.yml` and `.env` are correct.
- **Rebuilding Containers:**  
  ```bash
  docker-compose down -v
  docker-compose up --build
  ```
- **Logs:**  
  ```bash
  docker-compose logs backend
  docker-compose logs frontend
  docker-compose logs db
  ```

## 📚 Advanced Guides & API Reference

- See the `docs/` folder for:
  - [API Reference](docs/api-reference.md)
  - [Architecture](docs/architecture.md)
  - [Admin Guide](docs/admin-guide.md)
  - [User Guide](docs/user-guide.md)
  - [Setup Guide](docs/setup-guide.md)
  - [Troubleshooting](docs/troubleshooting.md)
  - [API Spec (OpenAPI)](docs/api_spec.yaml)

## 🌱 Environment Variables

All secrets and sensitive configuration are loaded via environment variables. **No secrets are hardcoded.**

A sample `.env` file is provided at `backend/env.example`. Use `generate-secrets.py` to create a secure `.env` file.

**Example (`backend/.env`):**
```env
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_NAME=cipherquest_db
DB_USER=root
DB_PASSWORD=your_secure_database_password_here

# Flask Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production-minimum-32-characters
JWT_SECRET_KEY=your-jwt-secret-key-change-this-in-production-minimum-32-characters

# Security Configuration
BCRYPT_LOG_ROUNDS=12
RATE_LIMIT_PER_MINUTE=60

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
CORS_METHODS=GET,POST,PUT,DELETE,OPTIONS
CORS_ALLOW_HEADERS=Content-Type,Authorization,X-Requested-With

# Docker
MYSQL_ROOT_PASSWORD=your_secure_mysql_root_password
```

**Example (`frontend/.env`):**
```env
REACT_APP_API_URL=http://localhost:5000/api
```

**See [backend/env.example](backend/env.example) for all available variables.**

---

## 🔒 Security Best Practices
- **All secrets are loaded from environment variables** (never hardcoded)
- **Comprehensive security headers** are set in both backend (Flask) and frontend (nginx)
- **CORS is restricted** to trusted origins
- **Rate limiting** is enabled on all API endpoints
- **Input validation** and **output encoding** are enforced
- **.env and other sensitive files are gitignored**
- **Automated security validation** with `security-check.py`
- **See [SECURITY.md](SECURITY.md) for full details and checklist**

---

## 📁 Project Structure

CipherQuest/
├── assets/
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── env.example
│   ├── .env  # (generated, gitignored)
│   ├── generate-secrets.py
│   ├── security-check.py
│   ├── SECURITY.md
│   ├── ...
├── frontend/
│   ├── nginx.conf
│   ├── ...
├── docker-compose.yml
├── .gitignore
├── README.md

---

## 🤝 Contributing
We welcome contributions from the community!
- See [CONTRIBUTING.md](CONTRIBUTING.md) and [docs/contributing.md](docs/contributing.md) for guidelines.
- Please follow the code of conduct in [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
- Open issues and pull requests to help improve CipherQuest.

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments
- **Fonts**: Google Fonts (Orbitron, Fira Code, Montserrat)
- **Icons**: Font Awesome
- **Animations**: GSAP (GreenSock)
- **Design Inspiration**: Cyberpunk aesthetics and modern web design trends

## 📞 Support
- **Issues**: Report bugs and feature requests via GitHub Issues
- **Discussions**: Join community discussions on GitHub Discussions
- **Email**: Contact the development team for support
  
*Hack. Learn. Level Up.*
