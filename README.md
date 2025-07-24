# Macro Tracking App 

A FastAPI-based backend for a macro tracking application with Supabase integration and real user authentication.

## Current Status

✅ **Phase 1 Complete**: Basic FastAPI setup with Supabase integration
✅ **Phase 2 Complete**: Real user authentication with Supabase Auth
✅ **Phase 3 Complete**: User profile management with JWT authentication

## Features

- **Real Authentication**: Supabase Auth integration with JWT tokens
- **User Management**: Signup, login, and profile creation
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
   Create a `.env` file with your Supabase credentials:
   ```env
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_anon_key
   ```

3. **Run the server:**
   ```bash
   python -m app.main
   ```

4. **Visit the API:**
   - Health: http://localhost:8000/health
   - Database Test: http://localhost:8000/test-table
   - API Docs: http://localhost:8000/docs
   - Authentication: http://localhost:8000/auth/signup

## API Endpoints

### Authentication
- `POST /auth/signup` - Create new user account
- `POST /auth/login` - Authenticate user
- `GET /auth/me` - Get current user (requires JWT)

### User Profiles
- `POST /profiles/` - Create user profile (requires JWT)

### Health & Testing
- `GET /health` - Server health check
- `GET /test-table` - Database connection test

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
│   │   └── profiles.py      # User profile endpoints
│   └── services/            # Business logic services
│       ├── __init__.py
│       └── auth_service.py  # Authentication service
├── docs/                    # Project documentation
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (not in git)
└── README.md               # This file
```

## Next Steps

- [ ] Add macro goals management
- [ ] Add food logging functionality
- [ ] Add agent permissions system
- [ ] Implement frontend React application 
