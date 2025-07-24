# API Endpoints Documentation

## Overview
This document describes all the API endpoints in the Macro Tracking App, what they do, and how they interact with the database.

---

## 🔍 Read/Test Endpoints (GET)

### `GET /`
**Purpose**: Basic health check to verify FastAPI is running
**Response**: Simple JSON with status message
**Database**: None
**Example Response**:
```json
{
  "message": "Hello! FastAPI is working!",
  "status": "success"
}
```

### `GET /health`
**Purpose**: Check if the server is healthy and running
**Response**: Server status information
**Database**: None
**Example Response**:
```json
{
  "status": "healthy",
  "message": "Server is running"
}
```

### `GET /test-db`
**Purpose**: Test the connection to Supabase database
**Response**: Database connection status
**Database**: Tests connection (no data read/written)
**Example Response**:
```json
{
  "status": "success",
  "message": " Database connection successful!",
  "database": "Supabase"
}
```

### `GET /test-table`
**Purpose**: Test reading from the user_profiles table
**Response**: Data from user_profiles table (currently empty)
**Database**: **READS** from `user_profiles` table
**Example Response**:
```json
{
  "status": "success",
  "message": " Successfully connected to user_profiles table!",
  "data": [],
  "count": 0
}
```

### `GET /me`
**Purpose**: Get current user information (DUMMY - for testing)
**Response**: Dummy user data
**Database**: None (dummy data)
**Example Response**:
```json
{
  "id": "user_123",
  "email": "user@example.com",
  "message": "This is dummy user data for Phase 1"
}
```

---

## ✏️ Create Endpoints (POST)

### `POST /user-profiles`
**Purpose**: Create a new user profile in the database
**Request Body**: UserProfileCreate model
**Response**: UserProfileResponse with created data
**Database**: **WRITES** to `user_profiles` table
**Status Code**: 201 (Created)

**Request Example**:
```json
{
  "user_id": "test-user-123",
  "display_name": "Test User"
}
```

**Response Example**:
```json
{
  "user_id": "test-user-123",
  "display_name": "Test User",
  "created_at": "2025-01-22T10:30:00Z",
  "updated_at": "2025-01-22T10:30:00Z"
}
```

### `POST /signup`
**Purpose**: Create a new user account (DUMMY - for testing)
**Request Body**: UserSignupRequest model
**Response**: TokenResponse with dummy token
**Database**: None (dummy implementation)
**Status Code**: 201 (Created)

**Request Example**:
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response Example**:
```json
{
  "access_token": "dummy_token_12345",
  "token_type": "bearer",
  "user_id": "user_123",
  "email": "user@example.com"
}
```

### `POST /login`
**Purpose**: Authenticate user and return token (DUMMY - for testing)
**Request Body**: UserLoginRequest model
**Response**: TokenResponse with dummy token
**Database**: None (dummy implementation)

**Request Example**:
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response Example**:
```json
{
  "access_token": "dummy_token_12345",
  "token_type": "bearer",
  "user_id": "user_123",
  "email": "user@example.com"
}
```

---

## 🔄 Database Interaction Summary

| Endpoint | Method | Database Action | Purpose |
|----------|--------|-----------------|---------|
| `/` | GET | None | Health check |
| `/health` | GET | None | Server status |
| `/test-db` | GET | Test connection | Database connectivity |
| `/test-table` | GET | **READ** user_profiles | Test table access |
| `/me` | GET | None | Get user info (dummy) |
| `/user-profiles` | POST | **WRITE** user_profiles | Create user profile |
| `/signup` | POST | None | User registration (dummy) |
| `/login` | POST | None | User authentication (dummy) |

---

## 🚧 Future Endpoints (Planned)

### Authentication (Real Implementation)
- `POST /auth/signup` - Real user registration
- `POST /auth/login` - Real user authentication
- `POST /auth/logout` - User logout
- `GET /auth/me` - Get current user (with JWT)

### Macro Management
- `POST /macros` - Set user macro goals
- `GET /macros` - Get user macro goals
- `PUT /macros` - Update macro goals

### Food Logging
- `POST /food-log` - Log a meal
- `GET /food-log` - Get food logs
- `DELETE /food-log/{id}` - Delete a food log

### Agent Management
- `POST /agent-consent` - Grant agent access
- `GET /agent-consent` - Check agent permissions 