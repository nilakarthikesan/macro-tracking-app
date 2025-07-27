# Macro Tracking App 

A FastAPI-based backend for a macro tracking application with Supabase integration, real user authentication, and SendGrid email functionality.

## Current Status

**Phase 1 Complete**: Basic FastAPI setup with Supabase integration
**Phase 2 Complete**: Real user authentication with Supabase Auth
**Phase 3 Complete**: User profile management with JWT authentication
**Phase 4 Complete**: Macro goals management with CRUD operations
**Phase 5 Complete**: Food logging functionality with full CRUD operations
**Phase 6 Complete**: SendGrid email integration with welcome and password reset emails

## Features

- **Real Authentication**: Supabase Auth integration with JWT tokens
- **User Management**: Signup, login, and profile creation
- **Email Integration**: SendGrid-powered welcome emails and password reset functionality
- **Macro Goals Management**: Set and track daily macro targets
- **Food Logging**: Complete CRUD operations for logging meals and snacks
- **Daily & Weekly Summaries**: Track progress with goal comparisons
- **Database Integration**: PostgreSQL via Supabase
- **Organized Code**: Modular FastAPI routers
- **API Documentation**: Auto-generated with FastAPI
- **Health Monitoring**: Server and database health checks

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Setup:**
   Create a `.env` file with your credentials:
   ```env
   # Supabase Configuration
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_anon_key
   
   # SendGrid Configuration
   SENDGRID_API_KEY=your_sendgrid_api_key
   FROM_EMAIL=noreply@macro.works
   FROM_NAME=Macro Tracking App
   
   # JWT Configuration (optional)
   JWT_SECRET_KEY=your-secret-key-change-in-production
   ```

3. **Run the server:**
   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Visit the API:**
   - Health: http://localhost:8000/health
   - API Docs: http://localhost:8000/docs
   - SendGrid Test: http://localhost:8000/emails/test-sendgrid

## API Endpoints

### Authentication
- `POST /auth/signup` - Create new user account (sends welcome email)
- `POST /auth/login` - Authenticate user
- `POST /auth/password-reset` - Request password reset email
- `GET /auth/me` - Get current user (requires JWT)

### User Profiles
- `POST /profiles/` - Create user profile (requires JWT)

### Macro Goals
- `POST /macro-goals/` - Create or update macro goals (requires JWT)
- `GET /macro-goals/` - Get current macro goals (requires JWT)
- `PUT /macro-goals/` - Update macro goals (partial update, requires JWT)

### Food Logging
- `POST /food-logs/` - Log a new food item (requires JWT)
- `GET /food-logs/` - Get all food logs for current user (requires JWT)
- `PUT /food-logs/{log_id}` - Update a food log entry (requires JWT)
- `DELETE /food-logs/{log_id}` - Delete a food log entry (requires JWT)
- `GET /food-logs/summary/daily` - Get daily macro summary with goal comparison (requires JWT)
- `GET /food-logs/summary/weekly` - Get weekly macro summary with averages (requires JWT)

### Email Services
- `GET /emails/test-sendgrid` - Test SendGrid connection

### Health & Testing
- `GET /health` - Server health check
- `GET /test-table` - Database connection test

## Email Features

### Welcome Emails
- Automatically sent when users sign up
- Includes getting started guide
- HTML formatted with app branding

### Password Reset Emails
- Secure password reset functionality
- Includes reset link (frontend integration ready)
- Professional email templates

### SendGrid Integration
- Reliable email delivery
- Professional sender domain (noreply@macro.works)
- HTML email templates
- Error handling and logging

## Project Structure

```
macro-tracking-app/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Environment configuration
│   ├── database.py          # Supabase client setup
│   ├── models.py            # Pydantic models
│   ├── routers/             # API route modules
│   │   ├── health.py        # Health check endpoints
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── profiles.py      # User profile endpoints
│   │   ├── macro_goals.py   # Macro goals endpoints
│   │   ├── food_logs.py     # Food logging endpoints
│   │   └── emails.py        # Email testing endpoints
│   └── services/            # Business logic services
│       ├── __init__.py
│       ├── auth_service.py  # Authentication service
│       └── email_service.py # SendGrid email service
├── docs/                    # Project documentation
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (not in git)
└── README.md               # This file
```

## Database Schema

### Core Tables
- `auth.users` - User authentication (Supabase Auth)
- `user_profiles` - User profile information
- `macro_goals` - User macro goals and targets
- `food_logs` - Food logging entries with macros

### Relationships
- All tables linked to `auth.users.id` via foreign keys
- Row Level Security (RLS) policies for data isolation
- Proper indexing for performance

## Next Steps

- [ ] **Frontend Development**: React.js application with authentication
- [ ] **Email Templates**: Customize email designs and branding
- [ ] **Production Deployment**: Deploy to production environment
- [ ] **Testing Suite**: Comprehensive API and integration tests
- [ ] **Monitoring**: Add logging and performance monitoring

## Development Notes

### Email Configuration
- SendGrid API key required for email functionality
- Domain authentication completed (noreply@macro.works)
- HTML email templates implemented
- Error handling prevents email failures from breaking core functionality

### Authentication Flow
1. User signs up → Account created in Supabase Auth
2. Welcome email sent automatically
3. User logs in → JWT token issued
4. Protected endpoints require valid JWT
5. Password reset available via email

### API Security
- JWT-based authentication for protected endpoints
- Input validation with Pydantic models
- Error handling with proper HTTP status codes
- Database queries protected with user isolation 
