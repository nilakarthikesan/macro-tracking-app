# API Endpoints Documentation

## Overview
This document describes all the API endpoints in the Macro Tracking App, what they do, and how they interact with the database.

---

## Read/Test Endpoints (GET)

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

### `GET /macro-goals/`
**Purpose**: Get current user's macro goals
**Headers**: `Authorization: Bearer <jwt_token>`
**Response**: User's macro goals data
**Database**: **READS** from `macro_goals` table
**Example Response**:
```json
{
  "user_id": "b7bcb761-e36b-4f65-ae62-da2451005f32",
  "total_calories": 2000,
  "protein_pct": 30.0,
  "carb_pct": 40.0,
  "fat_pct": 30.0,
  "created_at": "2025-07-24T04:05:56.8207",
  "updated_at": "2025-07-24T04:05:56.8207"
}
```

### `GET /food-logs/`
**Purpose**: Get all food logs for the current user
**Headers**: `Authorization: Bearer <jwt_token>`
**Response**: Array of food log entries
**Database**: **READS** from `food_logs` table
**Example Response**:
```json
[
  {
    "id": "da31eb61-6ec3-400f-b36e-cb83807c71e",
    "user_id": "b7bcb761-e36b-4f65-ae62-da2451005f32",
    "meal_type": "breakfast",
    "food_name": "Oatmeal with berries",
    "calories": 250,
    "protein": 8.5,
    "carbs": 45.2,
    "fat": 4.1,
    "logged_at": "2025-07-25T05:00:25.010699",
    "created_at": "2025-07-25T05:00:25.010699",
    "updated_at": "2025-07-25T05:00:25.010699"
  }
]
```

### `GET /food-logs/summary/daily`
**Purpose**: Get daily macro summary with goal comparison
**Headers**: `Authorization: Bearer <jwt_token>`
**Query Parameters**: `date` (optional, YYYY-MM-DD format, defaults to today)
**Response**: Daily summary with totals, goals, and remaining macros
**Database**: **READS** from `food_logs` and `macro_goals` tables
**Example Response**:
```json
{
  "date": "2025-07-25",
  "total_calories": 400,
  "total_protein": 35.0,
  "total_carbs": 10.0,
  "total_fat": 18.0,
  "goal_calories": 2200,
  "goal_protein": 192.5,
  "goal_carbs": 220.0,
  "goal_fat": 73.3,
  "calories_remaining": 1800,
  "protein_remaining": 157.5,
  "carbs_remaining": 210.0,
  "fat_remaining": 55.3,
  "meals": [
    {
      "meal_type": "lunch",
      "calories": 400,
      "protein": 35.0,
      "carbs": 10.0,
      "fat": 18.0
    }
  ]
}
```

### `GET /food-logs/summary/weekly`
**Purpose**: Get weekly macro summary with averages
**Headers**: `Authorization: Bearer <jwt_token>`
**Query Parameters**: `week_start` (optional, YYYY-MM-DD format, defaults to current week)
**Response**: Weekly summary with daily averages and goal comparison
**Database**: **READS** from `food_logs` and `macro_goals` tables
**Example Response**:
```json
{
  "week_start": "2025-07-21",
  "week_end": "2025-07-27",
  "total_calories": 2800,
  "total_protein": 245.0,
  "total_carbs": 280.0,
  "total_fat": 93.3,
  "daily_averages": {
    "calories": 400.0,
    "protein": 35.0,
    "carbs": 40.0,
    "fat": 13.3
  },
  "goal_calories": 2200,
  "goal_protein": 192.5,
  "goal_carbs": 220.0,
  "goal_fat": 73.3,
  "daily_totals": {
    "2025-07-25": {
      "calories": 400,
      "protein": 35.0,
      "carbs": 40.0,
      "fat": 13.3
    }
  }
}
```

### `GET /emails/test-sendgrid`
**Purpose**: Test SendGrid email connection
**Response**: Email test results
**External Service**: **SENDS** email via SendGrid
**Example Response**:
```json
{
  "success": true,
  "message": "SendGrid connection test successful! Email sent to test@example.com",
  "details": {
    "success": true,
    "message": "SendGrid connection test successful",
    "status_code": 202,
    "message_id": "pLJEu4bRTm0mzSf58vYGTQ"
  }
}
```

---

## Create Endpoints (POST)

### `POST /auth/signup`
**Purpose**: Create new user account with welcome email
**Request Body**: UserSignupRequest model
**Response**: TokenResponse with user data
**Database**: **WRITES** to Supabase Auth (auth.users)
**External Service**: **SENDS** welcome email via SendGrid
**Status Code**: 201 (Created)

**Request Example**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response Example**:
```json
{
  "access_token": "signup_successful",
  "token_type": "bearer",
  "user_id": "b7bcb761-e36b-4f65-ae62-da2451005f32",
  "email": "user@example.com"
}
```

**Email Sent**: Welcome email with getting started guide

### `POST /auth/login`
**Purpose**: Authenticate user and return access token
**Request Body**: UserLoginRequest model
**Response**: TokenResponse with JWT token
**Database**: **READS** from Supabase Auth (auth.users)
**Status Code**: 200 (OK)

**Request Example**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response Example**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": "b7bcb761-e36b-4f65-ae62-da2451005f32",
  "email": "user@example.com"
}
```

### `POST /auth/password-reset`
**Purpose**: Request password reset email
**Request Body**: PasswordResetRequest model
**Response**: Success message
**External Service**: **SENDS** password reset email via SendGrid
**Status Code**: 200 (OK)

**Request Example**:
```json
{
  "email": "user@example.com"
}
```

**Response Example**:
```json
{
  "success": true,
  "message": "Password reset email sent successfully"
}
```

**Email Sent**: Password reset email with reset link

### `POST /profiles/`
**Purpose**: Create user profile for authenticated user
**Headers**: `Authorization: Bearer <jwt_token>`
**Request Body**: ProfileCreate model
**Response**: ProfileResponse with created data
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

### `POST /macro-goals/`
**Purpose**: Create or update macro goals for the current user
**Headers**: `Authorization: Bearer <jwt_token>`
**Request Body**: MacroGoalsCreate model
**Response**: MacroGoalsResponse with created/updated data
**Database**: **WRITES** to `macro_goals` table
**Status Code**: 201 (Created)

**Request Example**:
```json
{
  "total_calories": 2000,
  "protein_pct": 30.0,
  "carb_pct": 40.0,
  "fat_pct": 30.0
}
```

**Response Example**:
```json
{
  "user_id": "b7bcb761-e36b-4f65-ae62-da2451005f32",
  "total_calories": 2000,
  "protein_pct": 30.0,
  "carb_pct": 40.0,
  "fat_pct": 30.0,
  "created_at": "2025-07-24T04:05:56.8207",
  "updated_at": "2025-07-24T04:05:56.8207"
}
```

### `POST /food-logs/`
**Purpose**: Log a new food item for the current user
**Headers**: `Authorization: Bearer <jwt_token>`
**Request Body**: FoodLogCreate model
**Response**: FoodLogResponse with created data
**Database**: **WRITES** to `food_logs` table
**Status Code**: 201 (Created)

**Request Example**:
```json
{
  "meal_type": "breakfast",
  "food_name": "Oatmeal with berries",
  "calories": 250,
  "protein": 8.5,
  "carbs": 45.2,
  "fat": 4.1
}
```

**Response Example**:
```json
{
  "id": "da31eb61-6ec3-400f-b36e-cb83807c71e",
  "user_id": "b7bcb761-e36b-4f65-ae62-da2451005f32",
  "meal_type": "breakfast",
  "food_name": "Oatmeal with berries",
  "calories": 250,
  "protein": 8.5,
  "carbs": 45.2,
  "fat": 4.1,
  "logged_at": "2025-07-25T05:00:25.010699",
  "created_at": "2025-07-25T05:00:25.010699",
  "updated_at": "2025-07-25T05:00:25.010699"
}
```

---

## Update Endpoints (PUT)

### `PUT /macro-goals/`
**Purpose**: Update macro goals for the current user (partial update)
**Headers**: `Authorization: Bearer <jwt_token>`
**Request Body**: MacroGoalsUpdate model (all fields optional)
**Response**: MacroGoalsResponse with updated data
**Database**: **UPDATES** `macro_goals` table
**Status Code**: 200 (OK)

**Request Example**:
```json
{
  "total_calories": 2200,
  "protein_pct": 35.0
}
```

**Response Example**:
```json
{
  "user_id": "b7bcb761-e36b-4f65-ae62-da2451005f32",
  "total_calories": 2200,
  "protein_pct": 35.0,
  "carb_pct": 40.0,
  "fat_pct": 30.0,
  "created_at": "2025-07-24T04:05:56.8207",
  "updated_at": "2025-07-25T01:29:54.123456"
}
```

### `PUT /food-logs/{log_id}`
**Purpose**: Update a specific food log entry
**Headers**: `Authorization: Bearer <jwt_token>`
**Path Parameters**: `log_id` (UUID of the food log)
**Request Body**: FoodLogUpdate model (all fields optional)
**Response**: FoodLogResponse with updated data
**Database**: **UPDATES** `food_logs` table
**Status Code**: 200 (OK)

**Request Example**:
```json
{
  "calories": 300,
  "protein": 10.0
}
```

**Response Example**:
```json
{
  "id": "da31eb61-6ec3-400f-b36e-cb83807c71e",
  "user_id": "b7bcb761-e36b-4f65-ae62-da2451005f32",
  "meal_type": "breakfast",
  "food_name": "Oatmeal with berries",
  "calories": 300,
  "protein": 10.0,
  "carbs": 45.2,
  "fat": 4.1,
  "logged_at": "2025-07-25T05:00:25.010699",
  "created_at": "2025-07-25T05:00:25.010699",
  "updated_at": "2025-07-25T05:15:30.123456"
}
```

---

## Delete Endpoints (DELETE)

### `DELETE /food-logs/{log_id}`
**Purpose**: Delete a specific food log entry
**Headers**: `Authorization: Bearer <jwt_token>`
**Path Parameters**: `log_id` (UUID of the food log)
**Response**: No content
**Database**: **DELETES** from `food_logs` table
**Status Code**: 204 (No Content)

**Example**: `DELETE /food-logs/da31eb61-6ec3-400f-b36e-cb83807c71e`

---

## Database Interaction Summary

| Endpoint | Method | Database Action | Authentication | External Service | Purpose |
|----------|--------|-----------------|----------------|------------------|---------|
| `/health` | GET | None | None | None | Server health check |
| `/test-table` | GET | **READ** user_profiles | None | None | Test table access |
| `/auth/me` | GET | **READ** auth.users | JWT Required | None | Get current user |
| `/macro-goals/` | GET | **READ** macro_goals | JWT Required | None | Get macro goals |
| `/food-logs/` | GET | **READ** food_logs | JWT Required | None | Get food logs |
| `/food-logs/summary/daily` | GET | **READ** food_logs, macro_goals | JWT Required | None | Get daily summary |
| `/food-logs/summary/weekly` | GET | **READ** food_logs, macro_goals | JWT Required | None | Get weekly summary |
| `/emails/test-sendgrid` | GET | None | None | **SEND** email | Test SendGrid |
| `/auth/signup` | POST | **WRITE** auth.users | None | **SEND** welcome email | User registration |
| `/auth/login` | POST | **READ** auth.users | None | None | User authentication |
| `/auth/password-reset` | POST | None | None | **SEND** reset email | Password reset |
| `/profiles/` | POST | **WRITE** user_profiles | JWT Required | None | Create user profile |
| `/macro-goals/` | POST | **WRITE** macro_goals | JWT Required | None | Create/update macro goals |
| `/food-logs/` | POST | **WRITE** food_logs | JWT Required | None | Create food log |
| `/macro-goals/` | PUT | **UPDATE** macro_goals | JWT Required | None | Update macro goals |
| `/food-logs/{log_id}` | PUT | **UPDATE** food_logs | JWT Required | None | Update food log |
| `/food-logs/{log_id}` | DELETE | **DELETE** food_logs | JWT Required | None | Delete food log |

---

## Authentication Flow

1. **User Registration**: `POST /auth/signup` → Creates user in Supabase Auth + sends welcome email
2. **User Login**: `POST /auth/login` → Returns JWT token
3. **Password Reset**: `POST /auth/password-reset` → Sends reset email
4. **Protected Endpoints**: Include `Authorization: Bearer <jwt_token>` header
5. **User Profile**: `POST /profiles/` → Creates profile linked to authenticated user

---

## Email Integration

### SendGrid Configuration
- **API Key**: Required in environment variables
- **Sender Domain**: noreply@macro.works (authenticated)
- **Templates**: HTML emails with app branding

### Email Types
1. **Welcome Emails**: Sent automatically on signup
2. **Password Reset**: Sent on password reset request
3. **Test Emails**: Available via `/emails/test-sendgrid`

### Email Features
- HTML formatting with professional design
- Error handling (email failures don't break core functionality)
- Message tracking via SendGrid message IDs
- Configurable sender information

---

## Future Endpoints (Planned)

### Agent Management
- `POST /agent-consent` - Grant agent access
- `GET /agent-consent` - Check agent permissions
- `DELETE /agent-consent` - Revoke agent access

### Advanced Analytics
- `GET /analytics/trends` - Long-term macro trends
- `GET /analytics/comparison` - Compare periods
- `GET /analytics/recommendations` - AI-powered suggestions

### User Preferences
- `POST /preferences` - Set user preferences
- `GET /preferences` - Get user preferences
- `PUT /preferences` - Update user preferences 