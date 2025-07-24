# API Endpoints Documentation

## Overview
This document describes all the API endpoints in the Macro Tracking App, what they do, and how they interact with the database.

---

## 🔍 Read/Test Endpoints (GET)

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

### `GET /test-table`
**Purpose**: Test reading from the user_profiles table
**Response**: Data from user_profiles table
**Database**: **READS** from `user_profiles` table
**Example Response**:
```json
{
  "status": "success",
  "message": "Successfully connected to user_profiles table!",
  "data": [
    {
      "user_id": "b7bcb761-e36b-4f65-ae62-da2451005f32",
      "display_name": "Test User Profile",
      "created_at": "2025-07-24T04:05:56.8207",
      "updated_at": "2025-07-24T04:05:56.8207"
    }
  ],
  "count": 1
}
```

### `GET /auth/me`
**Purpose**: Get current user information from JWT token
**Headers**: `Authorization: Bearer <jwt_token>`
**Response**: Current user data from Supabase Auth
**Database**: **READS** from Supabase Auth (auth.users)
**Example Response**:
```json
{
  "id": "b7bcb761-e36b-4f65-ae62-da2451005f32",
  "email": "test@macroapp.com",
  "message": "Real user data from Supabase Auth"
}
```

---

## ✏️ Create Endpoints (POST)

### `POST /auth/signup`
**Purpose**: Create a new user account using Supabase Auth
**Request Body**: UserSignupRequest model
**Response**: TokenResponse with user info
**Database**: **WRITES** to Supabase Auth (auth.users)
**Status Code**: 201 (Created)

**Request Example**:
```json
{
  "email": "newuser@example.com",
  "password": "securepassword123"
}
```

**Response Example**:
```json
{
  "access_token": "signup_successful",
  "token_type": "bearer",
  "user_id": "b7bcb761-e36b-4f65-ae62-da2451005f32",
  "email": "newuser@example.com"
}
```

### `POST /auth/login`
**Purpose**: Authenticate user and return access token
**Request Body**: UserLoginRequest model
**Response**: TokenResponse with JWT token
**Database**: **READS** from Supabase Auth (auth.users)

**Request Example**:
```json
{
  "email": "test@macroapp.com",
  "password": "test123"
}
```

**Response Example**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsImtpZCI6IjlVMEI2WGZwQitpTmtiU0IiLCJ0eXAiOiJKV1QifQ...",
  "token_type": "bearer",
  "user_id": "b7bcb761-e36b-4f65-ae62-da2451005f32",
  "email": "test@macroapp.com"
}
```

### `POST /profiles/`
**Purpose**: Create a new user profile in the database
**Headers**: `Authorization: Bearer <jwt_token>`
**Request Body**: UserProfileCreate model
**Response**: UserProfileResponse with created data
**Database**: **WRITES** to `user_profiles` table
**Status Code**: 201 (Created)

**Request Example**:
```json
{
  "display_name": "John Doe"
}
```

**Response Example**:
```json
{
  "user_id": "b7bcb761-e36b-4f65-ae62-da2451005f32",
  "display_name": "John Doe",
  "created_at": "2025-07-24T04:05:56.8207",
  "updated_at": "2025-07-24T04:05:56.8207"
}
```

---

## 🔄 Database Interaction Summary

| Endpoint | Method | Database Action | Authentication | Purpose |
|----------|--------|-----------------|----------------|---------|
| `/health` | GET | None | None | Server health check |
| `/test-table` | GET | **READ** user_profiles | None | Test table access |
| `/auth/me` | GET | **READ** auth.users | JWT Required | Get current user |
| `/auth/signup` | POST | **WRITE** auth.users | None | User registration |
| `/auth/login` | POST | **READ** auth.users | None | User authentication |
| `/profiles/` | POST | **WRITE** user_profiles | JWT Required | Create user profile |

---

## 🔐 Authentication Flow

1. **User Registration**: `POST /auth/signup` → Creates user in Supabase Auth
2. **User Login**: `POST /auth/login` → Returns JWT token
3. **Protected Endpoints**: Include `Authorization: Bearer <jwt_token>` header
4. **User Profile**: `POST /profiles/` → Creates profile linked to authenticated user

---

## 🚧 Future Endpoints (Planned)

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