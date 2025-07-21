# CipherQuest Backend API

A comprehensive Flask-based backend for the CipherQuest CTF learning platform, featuring user authentication, module management, challenge tracking, and leaderboard functionality.

## 🚀 Features

- **User Authentication**: JWT-based authentication with OAuth support (Google/GitHub)

- **Learning Modules**: Structured learning content with progress tracking

- **CTF Challenges**: Flag submission and validation system

- **Progress Tracking**: User progress across modules and challenges

- **Leaderboard**: Competitive ranking system

- **Admin Panel**: Content management and user administration

- **Security**: Rate limiting, input validation, and XSS prevention

## 🛠️ Tech Stack

- **Framework**: Flask 2.3.3

- **Database**: MySQL with SQLAlchemy ORM

- **Authentication**: JWT with Flask-JWT-Extended

- **Security**: Flask-Bcrypt, Flask-Limiter

- **Validation**: Custom validators with input sanitization

- **CORS**: Cross-origin resource sharing support

## 📋 Prerequisites

- Python 3.8+

- MySQL 8.0+

- pip (Python package manager)

## 🚀 Installation

1. **Clone the repository**

   ```bash
   cd backend
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   ```bash
   cp env.example .env
   # Edit .env with your configuration
   # For demo/testing, you can use the following OpenAI API key:
   # OPENAI_API_KEY=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
   # (Do NOT use this key in production. Obtain your own from https://platform.openai.com/account/api-keys)
   ```

5. **Create MySQL database**

   ```sql
   CREATE DATABASE cipherquest CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

6. **Initialize database**

   ```bash
   python init_db.py
   ```

7. **Run the application**

   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_NAME=cipherquest
DB_USER=root
DB_PASSWORD=your_password

# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-super-secret-key-change-this-in-production

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret-key-change-this-in-production
JWT_ACCESS_TOKEN_EXPIRES=3600
JWT_REFRESH_TOKEN_EXPIRES=604800

# OAuth Configuration (Optional)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret

# Security Configuration
BCRYPT_LOG_ROUNDS=12
RATE_LIMIT_PER_MINUTE=60

# OpenAI API Key (for demo/testing only)
OPENAI_API_KEY=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
# (Do NOT use this key in production. Obtain your own from https://platform.openai.com/account/api-keys)
```

## 📚 API Documentation

### Authentication Endpoints

#### POST `/api/auth/register`

Register a new user account.

**Request Body:**

```json
{
  "username": "hacker123",
  "email": "hacker@example.com",
  "password": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response:**

```json
{
  "message": "User registered successfully",
  "user": { ... },
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### POST `/api/auth/login`

Authenticate user and get access tokens.

**Request Body:**

```json
{
  "username": "hacker123",
  "password": "SecurePass123!"
}
```

#### POST `/api/auth/refresh`

Refresh access token using refresh token.

**Headers:**

```http
Authorization: Bearer <refresh_token>
```

### User Endpoints

#### GET `/api/user/profile`

Get current user profile.

**Headers:**

```http
Authorization: Bearer <access_token>
```

#### PUT `/api/user/profile`

Update user profile.

**Request Body:**

```json
{
  "first_name": "John",
  "last_name": "Smith",
  "bio": "Security enthusiast"
}
```

#### GET `/api/user/progress`

Get user progress across all modules and challenges.

### Module Endpoints

#### GET `/api/modules`

Get all learning modules with optional filtering.

**Query Parameters:**

- `category`: Filter by category
- `difficulty`: Filter by difficulty
- `limit`: Number of results (default: 50)
- `offset`: Pagination offset (default: 0)

#### GET `/api/modules/{module_id}`

Get specific module details with challenges.

#### POST `/api/modules/{module_id}/complete`

Mark module as completed.

### Challenge Endpoints

#### GET `/api/challenges`

Get all CTF challenges with optional filtering.

**Query Parameters:**

- `category`: Filter by category
- `difficulty`: Filter by difficulty
- `module_id`: Filter by module
- `limit`: Number of results
- `offset`: Pagination offset

#### GET `/api/challenges/{challenge_id}`

Get specific challenge details.

#### POST `/api/challenges/{challenge_id}/submit`

Submit flag for a challenge.

**Request Body:**

```json
{
  "flag": "flag{correct_answer}"
}
```

#### GET `/api/challenges/{challenge_id}/hint`

Get hint for a challenge.

### Leaderboard Endpoints

#### GET `/api/leaderboard`

Get leaderboard rankings.

#### GET `/api/leaderboard/top`

Get top players.

#### GET `/api/leaderboard/my-rank`

Get current user's rank.

### Admin Endpoints

#### GET `/api/admin/dashboard`

Get admin dashboard statistics.

#### GET `/api/admin/users`

Get all users (admin only).

#### POST `/api/admin/modules`

Create new module (admin only).

#### POST `/api/admin/challenges`

Create new challenge (admin only).

## 🔒 Security Features

### Rate Limiting

- Authentication endpoints: 5-10 requests per minute
- Flag submission: 20 requests per minute
- General endpoints: 50 requests per hour

### Input Validation

- Email format validation
- Password strength requirements
- Username format validation
- Flag format validation
- XSS prevention through input sanitization

### JWT Security

- Access tokens expire in 1 hour
- Refresh tokens expire in 7 days
- Secure token storage and transmission

## 🗄️ Database Schema

### Users Table

- User authentication and profile information
- OAuth integration support
- Experience and level tracking

### Modules Table

- Learning content and metadata
- Category and difficulty classification
- Estimated completion time

### Challenges Table

- CTF challenge details
- Hints and file attachments
- Module association

### Flags Table

- Challenge solutions
- Multiple flag types (exact, regex, contains)
- Point values

### User Progress Table

- Progress tracking for modules and challenges
- Completion status and timestamps
- Attempt counts and time spent

### Leaderboard Table

- User rankings and scores
- Completion statistics
- Rank calculations

## 🧪 Testing

### Manual Testing with curl

1. **Register a user:**

   ```bash
   curl -X POST http://localhost:5000/api/auth/register \
     -H "Content-Type: application/json" \
     -d '{"username":"testuser","email":"test@example.com","password":"TestPass123!"}'
   ```

2. **Login:**

   ```bash
   curl -X POST http://localhost:5000/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"username":"testuser","password":"TestPass123!"}'
   ```

3. **Get modules (with token):**

   ```bash
   curl -X GET http://localhost:5000/api/modules \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
   ```

### Postman Collection

Import the provided Postman collection for comprehensive API testing.

## 🚀 Deployment

### Production Setup

1. **Use production WSGI server:**

   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Set production environment:**

   ```bash
   export FLASK_ENV=production
   ```

3. **Use HTTPS in production**

4. **Set strong secret keys**

5. **Configure proper database credentials**

6. **Set up logging and monitoring**

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## 🤝 Contributing

1. Fork the repository

2. Create a feature branch

3. Make your changes

4. Add tests if applicable

5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation
- Review the example requests

## 🔄 Updates

- **v1.0.0**: Initial release with core functionality
- Authentication system with JWT
- Module and challenge management
- Progress tracking and leaderboard
- Admin panel for content management