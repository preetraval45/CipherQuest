# CipherQuest Setup Guide

## Prerequisites
- Python 3.8+
- Node.js 18+
- MySQL 8.0+
- npm

## Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy and edit environment variables:
   ```bash
   cp env.example .env
   # Edit .env with your DB and secret keys
   ```
5. Create the MySQL database:
   ```sql
   CREATE DATABASE cipherquest CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
6. Initialize the database:
   ```bash
   python init_db.py
   ```
7. Run the backend:
   ```bash
   python run.py
   ```

## Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Create a `.env` file and set your API URL:
   ```env
   REACT_APP_API_URL=http://localhost:5000
   ```
4. Run the frontend:
   ```bash
   npm start
   ```

## Access
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

---

For more details, see the backend README and API reference. 