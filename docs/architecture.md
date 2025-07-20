# CipherQuest Architecture Documentation

## 🏗️ System Architecture

### High-Level Architecture

```mermaid
graph TB
    subgraph "Frontend Layer"
        UI[React Frontend]
        Mobile[Mobile App]
    end
    
    subgraph "API Gateway"
        Gateway[API Gateway]
        Auth[Authentication]
        RateLimit[Rate Limiting]
    end
    
    subgraph "Backend Services"
        UserService[User Service]
        ModuleService[Module Service]
        ChallengeService[Challenge Service]
        AIService[AI Tutor Service]
        LeaderboardService[Leaderboard Service]
    end
    
    subgraph "Data Layer"
        MySQL[(MySQL Database)]
        Redis[(Redis Cache)]
        FileStorage[File Storage]
    end
    
    subgraph "External Services"
        OAuth[OAuth Providers]
        EmailService[Email Service]
        PaymentService[Payment Gateway]
    end
    
    UI --> Gateway
    Mobile --> Gateway
    Gateway --> Auth
    Gateway --> RateLimit
    Auth --> UserService
    RateLimit --> UserService
    RateLimit --> ModuleService
    RateLimit --> ChallengeService
    RateLimit --> AIService
    RateLimit --> LeaderboardService
    
    UserService --> MySQL
    ModuleService --> MySQL
    ChallengeService --> MySQL
    AIService --> MySQL
    LeaderboardService --> MySQL
    
    UserService --> Redis
    ModuleService --> Redis
    ChallengeService --> Redis
    
    UserService --> FileStorage
    ModuleService --> FileStorage
    
    UserService --> OAuth
    UserService --> EmailService
    UserService --> PaymentService
```

### Technology Stack

#### Frontend
- **Framework**: React 18 with TypeScript
- **State Management**: Redux Toolkit
- **Styling**: CSS Modules + Tailwind CSS
- **Build Tool**: Vite
- **Testing**: Jest + React Testing Library

#### Backend
- **Framework**: Flask (Python)
- **Database ORM**: SQLAlchemy
- **Authentication**: JWT + OAuth2
- **API Documentation**: OpenAPI 3.0
- **Testing**: Pytest

#### Database
- **Primary**: MySQL 8.0
- **Cache**: Redis
- **File Storage**: AWS S3 / Local Storage

#### Infrastructure
- **Containerization**: Docker + Docker Compose
- **CI/CD**: GitHub Actions
- **Deployment**: Heroku, Vercel, Docker Hub
- **Monitoring**: Sentry, LogRocket

## 🔄 Data Flow Diagrams

### User Authentication Flow

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant A as Auth Service
    participant D as Database
    participant O as OAuth Provider
    
    U->>F: Enter credentials
    F->>A: POST /api/auth/login
    A->>D: Verify credentials
    D-->>A: User data
    A->>A: Generate JWT tokens
    A-->>F: Access + Refresh tokens
    F->>F: Store tokens
    F-->>U: Redirect to dashboard
    
    Note over U,O: OAuth Flow
    U->>F: Click OAuth button
    F->>O: Redirect to OAuth
    O-->>F: Authorization code
    F->>A: POST /api/auth/oauth
    A->>O: Exchange code for token
    O-->>A: User info
    A->>D: Create/update user
    A-->>F: JWT tokens
    F-->>U: Logged in
```

### Module Learning Flow

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant M as Module Service
    participant P as Progress Service
    participant D as Database
    participant AI as AI Tutor
    
    U->>F: Access module
    F->>M: GET /api/modules/{id}
    M->>D: Fetch module data
    D-->>M: Module content
    M->>P: Get user progress
    P->>D: Fetch progress
    D-->>P: Progress data
    M-->>F: Module + progress
    F-->>U: Display module
    
    U->>F: Complete module
    F->>M: POST /api/modules/{id}/complete
    M->>P: Update progress
    P->>D: Save completion
    M->>D: Award experience points
    M-->>F: Success response
    F-->>U: Module completed
```

### Challenge Submission Flow

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant C as Challenge Service
    participant P as Progress Service
    participant L as Leaderboard Service
    participant D as Database
    
    U->>F: Submit flag
    F->>C: POST /api/challenges/{id}/submit
    C->>C: Validate flag format
    C->>D: Check flag correctness
    D-->>C: Flag validation result
    
    alt Flag Correct
        C->>P: Update challenge progress
        P->>D: Mark as completed
        C->>L: Update leaderboard
        L->>D: Recalculate scores
        C-->>F: Success + points
        F-->>U: Flag accepted
    else Flag Incorrect
        C->>P: Increment attempts
        P->>D: Save attempt
        C-->>F: Incorrect flag
        F-->>U: Try again
    end
```

### AI Tutor Interaction Flow

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant AI as AI Service
    participant D as Database
    participant O as OpenAI API
    
    U->>F: Ask question
    F->>AI: POST /api/ai/chat
    AI->>D: Get conversation history
    D-->>AI: Previous messages
    AI->>O: Send prompt + context
    O-->>AI: AI response
    AI->>D: Save conversation
    AI-->>F: Formatted response
    F-->>U: Display answer
    
    Note over U,O: Follow-up Questions
    U->>F: Ask follow-up
    F->>AI: POST /api/ai/chat
    AI->>D: Get full conversation
    AI->>O: Send with context
    O-->>AI: Contextual response
    AI-->>F: Answer
    F-->>U: Display
```

## 🗄️ Database Schema

### Core Tables

```mermaid
erDiagram
    users {
        int id PK
        string username UK
        string email UK
        string password_hash
        string first_name
        string last_name
        string avatar_url
        int experience
        int level
        string rank
        boolean is_active
        boolean email_verified
        string oauth_provider
        string oauth_id
        datetime created_at
        datetime last_login
    }
    
    modules {
        int id PK
        string title
        string description
        string content
        string category
        string difficulty
        int points
        int order
        boolean is_active
        datetime created_at
        datetime updated_at
    }
    
    challenges {
        int id PK
        string title
        string description
        string category
        string difficulty
        int points
        int module_id FK
        boolean is_active
        datetime created_at
        datetime updated_at
    }
    
    flags {
        int id PK
        int challenge_id FK
        string flag_hash
        int points
        boolean is_active
    }
    
    user_progress {
        int id PK
        int user_id FK
        int module_id FK
        int challenge_id FK
        boolean completed
        datetime completed_at
        int attempts
        int time_spent
        int score
    }
    
    leaderboard_entries {
        int id PK
        int user_id FK
        int total_score
        int completed_modules
        int completed_challenges
        datetime last_activity
    }
    
    users ||--o{ user_progress : has
    modules ||--o{ user_progress : tracks
    challenges ||--o{ user_progress : tracks
    challenges ||--o{ flags : has
    users ||--o{ leaderboard_entries : has
```

## 🔐 Security Architecture

### Authentication & Authorization

```mermaid
graph TB
    subgraph "Authentication Flow"
        Login[User Login]
        OAuth[OAuth Login]
        JWT[JWT Token Generation]
        Refresh[Token Refresh]
    end
    
    subgraph "Authorization"
        RBAC[Role-Based Access Control]
        Permissions[Permission System]
        RateLimit[Rate Limiting]
    end
    
    subgraph "Security Measures"
        Encryption[Data Encryption]
        Validation[Input Validation]
        Sanitization[Output Sanitization]
        Audit[Audit Logging]
    end
    
    Login --> JWT
    OAuth --> JWT
    JWT --> RBAC
    RBAC --> Permissions
    Permissions --> RateLimit
    
    JWT --> Encryption
    Permissions --> Validation
    Validation --> Sanitization
    Sanitization --> Audit
```

### Data Protection

```mermaid
graph LR
    subgraph "Data at Rest"
        DB[(Encrypted Database)]
        Files[Encrypted Files]
        Backups[Encrypted Backups]
    end
    
    subgraph "Data in Transit"
        HTTPS[HTTPS/TLS]
        API[API Encryption]
        WebSocket[Secure WebSocket]
    end
    
    subgraph "Access Control"
        Auth[Authentication]
        RBAC[Role-Based Access]
        Audit[Audit Logging]
    end
    
    DB --> HTTPS
    Files --> API
    Backups --> WebSocket
    
    Auth --> DB
    RBAC --> Files
    Audit --> Backups
```

## 🚀 Deployment Architecture

### Production Environment

```mermaid
graph TB
    subgraph "Load Balancer"
        LB[NGINX Load Balancer]
    end
    
    subgraph "Application Servers"
        App1[App Server 1]
        App2[App Server 2]
        App3[App Server 3]
    end
    
    subgraph "Database Cluster"
        Master[(MySQL Master)]
        Slave1[(MySQL Slave 1)]
        Slave2[(MySQL Slave 2)]
    end
    
    subgraph "Cache Layer"
        Redis1[Redis Primary]
        Redis2[Redis Replica]
    end
    
    subgraph "Storage"
        S3[AWS S3]
        CDN[CloudFront CDN]
    end
    
    LB --> App1
    LB --> App2
    LB --> App3
    
    App1 --> Master
    App2 --> Master
    App3 --> Master
    
    Master --> Slave1
    Master --> Slave2
    
    App1 --> Redis1
    App2 --> Redis1
    App3 --> Redis1
    
    Redis1 --> Redis2
    
    App1 --> S3
    App2 --> S3
    App3 --> S3
    
    S3 --> CDN
```

### CI/CD Pipeline

```mermaid
graph LR
    subgraph "Development"
        Code[Code Changes]
        Tests[Unit Tests]
        Coverage[Code Coverage]
    end
    
    subgraph "CI/CD"
        Build[Docker Build]
        Security[Security Scan]
        Deploy[Deploy to Staging]
    end
    
    subgraph "Testing"
        Integration[Integration Tests]
        E2E[End-to-End Tests]
        Performance[Performance Tests]
    end
    
    subgraph "Production"
        Staging[Staging Environment]
        Production[Production Deployment]
        Monitoring[Monitoring & Alerts]
    end
    
    Code --> Tests
    Tests --> Coverage
    Coverage --> Build
    Build --> Security
    Security --> Deploy
    Deploy --> Integration
    Integration --> E2E
    E2E --> Performance
    Performance --> Staging
    Staging --> Production
    Production --> Monitoring
```

## 📊 Monitoring & Analytics

### System Monitoring

```mermaid
graph TB
    subgraph "Application Monitoring"
        APM[Application Performance]
        Errors[Error Tracking]
        Logs[Log Aggregation]
    end
    
    subgraph "Infrastructure Monitoring"
        CPU[CPU Usage]
        Memory[Memory Usage]
        Disk[Disk Usage]
        Network[Network Traffic]
    end
    
    subgraph "Business Metrics"
        Users[Active Users]
        Engagement[User Engagement]
        Revenue[Revenue Metrics]
        Growth[Growth Metrics]
    end
    
    subgraph "Alerting"
        Alerts[Alert System]
        Notifications[Notifications]
        Escalation[Escalation Rules]
    end
    
    APM --> Alerts
    Errors --> Alerts
    Logs --> Alerts
    
    CPU --> Alerts
    Memory --> Alerts
    Disk --> Alerts
    Network --> Alerts
    
    Users --> Alerts
    Engagement --> Alerts
    Revenue --> Alerts
    Growth --> Alerts
    
    Alerts --> Notifications
    Notifications --> Escalation
```

## 🔄 API Architecture

### RESTful API Design

```mermaid
graph TB
    subgraph "API Gateway"
        Gateway[API Gateway]
        Auth[Authentication]
        RateLimit[Rate Limiting]
        CORS[CORS Handling]
    end
    
    subgraph "Service Layer"
        UserAPI[User API]
        ModuleAPI[Module API]
        ChallengeAPI[Challenge API]
        AIAPI[AI API]
        LeaderboardAPI[Leaderboard API]
    end
    
    subgraph "Data Access"
        DAO[Data Access Objects]
        Cache[Cache Layer]
        DB[Database]
    end
    
    Gateway --> Auth
    Auth --> RateLimit
    RateLimit --> CORS
    
    CORS --> UserAPI
    CORS --> ModuleAPI
    CORS --> ChallengeAPI
    CORS --> AIAPI
    CORS --> LeaderboardAPI
    
    UserAPI --> DAO
    ModuleAPI --> DAO
    ChallengeAPI --> DAO
    AIAPI --> DAO
    LeaderboardAPI --> DAO
    
    DAO --> Cache
    DAO --> DB
```

## 🎯 Performance Optimization

### Caching Strategy

```mermaid
graph TB
    subgraph "Client-Side"
        Browser[Browser Cache]
        LocalStorage[Local Storage]
        SessionStorage[Session Storage]
    end
    
    subgraph "Application Cache"
        Redis[Redis Cache]
        Memcached[Memcached]
        CDN[CDN Cache]
    end
    
    subgraph "Database"
        QueryCache[Query Cache]
        ConnectionPool[Connection Pool]
        Indexes[Database Indexes]
    end
    
    Browser --> Redis
    LocalStorage --> Redis
    SessionStorage --> Redis
    
    Redis --> Memcached
    Memcached --> CDN
    
    CDN --> QueryCache
    QueryCache --> ConnectionPool
    ConnectionPool --> Indexes
```

---

This architecture documentation provides a comprehensive overview of the CipherQuest platform's technical design, data flows, and system components. For detailed implementation guides, refer to the specific service documentation. 