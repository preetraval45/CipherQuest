# Docker Setup for CipherQuest

This guide provides instructions for setting up and running CipherQuest using Docker.

## Prerequisites

- Docker and Docker Compose installed
- Docker Hub account (credentials provided)

## Configuration

### Database Configuration
- **Host**: localhost (or `db` when using Docker Compose)
- **User**: root
- **Password**: Arjun@231
- **Database**: cipherquest_db

### Docker Hub Credentials
- **Username**: preetraval45@gmail.com
- **Password**: Arjuntower@231

## Quick Start

### 1. Docker Hub Login
```bash
docker login -u preetraval45@gmail.com -p Arjuntower@231
```

### 2. Build and Run with Docker Compose
```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d --build
```

### 3. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **MySQL Database**: localhost:3306

## Services

### MySQL Database
- **Image**: mysql:8.0
- **Port**: 3306
- **Database**: cipherquest_db (auto-created)
- **Root Password**: Arjun@231
- **Volume**: db_data (persistent storage)

### Flask Backend
- **Port**: 5000
- **Environment Variables**:
  - DB_HOST=db
  - DB_USER=root
  - DB_PASSWORD=Arjun@231
  - DB_NAME=cipherquest_db
  - SECRET_KEY=your_secure_flask_secret

### React Frontend
- **Port**: 3000
- **Build**: Multi-stage build with nginx

## Manual Image Building and Pushing

### Using the provided script:
```bash
# Windows
docker-setup.bat

# Linux/Mac
./docker-setup.sh
```

### Manual commands:
```bash
# Build images
docker build -t preetraval45/cipherquest-backend:latest ./backend
docker build -t preetraval45/cipherquest-frontend:latest ./frontend

# Push to Docker Hub
docker push preetraval45/cipherquest-backend:latest
docker push preetraval45/cipherquest-frontend:latest
```

## Environment Variables

The application uses the following environment variables (configured in docker-compose.yml):

```env
DB_HOST=db
DB_PORT=3306
DB_NAME=cipherquest_db
DB_USER=root
DB_PASSWORD=Arjun@231
SECRET_KEY=your_secure_flask_secret
OPENAI_API_KEY=your_api_key_if_used
FLASK_APP=app.py
FLASK_ENV=development
```

## Troubleshooting

### Database Connection Issues
1. Ensure MySQL container is running: `docker-compose ps`
2. Check logs: `docker-compose logs db`
3. Wait for database to be ready (backend has built-in wait mechanism)

### Port Conflicts
If ports 3000, 5000, or 3306 are already in use, modify the ports in docker-compose.yml:

```yaml
ports:
  - "3001:3000"  # Frontend on 3001
  - "5001:5000"  # Backend on 5001
  - "3307:3306"  # MySQL on 3307
```

### Clean Up
```bash
# Stop and remove containers
docker-compose down

# Remove volumes (WARNING: This will delete database data)
docker-compose down -v

# Remove all unused containers, networks, and images
docker system prune -a
```

## Development

For development, the docker-compose.yml includes volume mounts for live code reloading:

- Backend: `./backend:/app`
- Frontend: `./frontend:/app`

Changes to the code will be reflected immediately without rebuilding containers.

## Production Deployment

For production deployment:

1. Update environment variables in docker-compose.yml
2. Set FLASK_ENV=production
3. Use proper SECRET_KEY and other sensitive values
4. Consider using Docker secrets for sensitive data
5. Set up proper logging and monitoring

## Security Notes

- Change default passwords in production
- Use Docker secrets for sensitive data
- Regularly update base images
- Monitor container logs for security issues
- Consider using a reverse proxy (nginx) for production 