@echo off
echo Logging into Docker Hub...
docker login -u preetraval45@gmail.com -p Arjuntower@231

if %errorlevel% neq 0 (
    echo Failed to login to Docker Hub
    exit /b 1
)

echo Successfully logged into Docker Hub

echo Building and pushing backend image...
docker build -t preetraval45/cipherquest-backend:latest ./backend
docker push preetraval45/cipherquest-backend:latest

echo Building and pushing frontend image...
docker build -t preetraval45/cipherquest-frontend:latest ./frontend
docker push preetraval45/cipherquest-frontend:latest

echo Docker images built and pushed successfully!
echo You can now run: docker-compose up --build 