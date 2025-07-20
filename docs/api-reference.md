# CipherQuest API Reference

## Authentication
- `POST /api/auth/register` — Register a new user
- `POST /api/auth/login` — Login and receive JWT tokens
- `POST /api/auth/refresh` — Refresh JWT access token

## User
- `GET /api/user/profile` — Get current user profile
- `PUT /api/user/profile` — Update user profile
- `GET /api/user/progress` — Get user progress

## Modules
- `GET /api/modules` — List all modules
- `GET /api/modules/{module_id}` — Get module details
- `POST /api/modules/{module_id}/complete` — Mark module as completed

## Challenges
- `GET /api/challenges` — List all challenges
- `GET /api/challenges/{challenge_id}` — Get challenge details
- `POST /api/challenges/{challenge_id}/submit` — Submit a flag
- `GET /api/challenges/{challenge_id}/hint` — Get a hint

## Leaderboard
- `GET /api/leaderboard` — Get leaderboard rankings
- `GET /api/leaderboard/top` — Get top players
- `GET /api/leaderboard/my-rank` — Get current user's rank

## Admin
- `GET /api/admin/dashboard` — Admin dashboard stats
- `GET /api/admin/users` — List all users
- `POST /api/admin/modules` — Create a new module
- `POST /api/admin/challenges` — Create a new challenge

---

For detailed request/response examples, see the backend README or Postman collection. 