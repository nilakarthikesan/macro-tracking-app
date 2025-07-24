# Pydantic Models Documentation

## Overview
This document describes all the Pydantic models used in the Macro Tracking App. These models define the structure and validation rules for data that flows through the API.

---

## Authentication Models

### `UserSignupRequest`
**Purpose**: Validates data when a user signs up for a new account
**Used By**: `POST /signup` endpoint

```python
class UserSignupRequest(BaseModel):
    email: EmailStr      # Must be a valid email format
    password: str        # Password string
```

**Example**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

### `UserLoginRequest`
**Purpose**: Validates data when a user logs in
**Used By**: `POST /login` endpoint

```python
class UserLoginRequest(BaseModel):
    email: EmailStr      # Must be a valid email format
    password: str        # Password string
```

**Example**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

### `TokenResponse`
**Purpose**: Defines the structure of authentication tokens returned to users
**Used By**: `POST /signup`, `POST /login` endpoints

```python
class TokenResponse(BaseModel):
    access_token: str    # JWT token for authentication
    token_type: str      # Usually "bearer"
    user_id: str         # User's unique identifier
    email: str           # User's email address
```

**Example**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com"
}
```

### `UserResponse`
**Purpose**: Defines the structure of user information returned by the API
**Used By**: `GET /me` endpoint

```python
class UserResponse(BaseModel):
    id: str              # User's unique identifier
    email: str           # User's email address
    message: str         # Additional message or status
```

**Example**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "message": "User authenticated successfully"
}
```

---

## 👤 User Profile Models

### `UserProfileCreate`
**Purpose**: Validates data when creating a new user profile
**Used By**: `POST /user-profiles` endpoint

```python
class UserProfileCreate(BaseModel):
    user_id: str                    # User's unique identifier (required)
    display_name: Optional[str] = None  # Optional display name
```

**Example**:
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "display_name": "John Doe"
}
```

### `UserProfileResponse`
**Purpose**: Defines the structure of user profile data returned by the API
**Used By**: `POST /user-profiles` endpoint (response)

```python
class UserProfileResponse(BaseModel):
    user_id: str                    # User's unique identifier
    display_name: Optional[str]     # User's display name (can be null)
    created_at: str                 # When the profile was created
    updated_at: str                 # When the profile was last updated
```

**Example**:
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "display_name": "John Doe",
  "created_at": "2025-01-22T10:30:00Z",
  "updated_at": "2025-01-22T10:30:00Z"
}
```

---

## 🥗 Future Models (Planned)

### `MacroGoals`
**Purpose**: Will validate user's macro nutrient goals
**Used By**: Future macro management endpoints

```python
class MacroGoals(BaseModel):
    total_calories: int     # Daily calorie target
    protein_pct: float      # Protein percentage (0-100)
    carb_pct: float         # Carbohydrate percentage (0-100)
    fat_pct: float          # Fat percentage (0-100)
```

**Example**:
```json
{
  "total_calories": 2000,
  "protein_pct": 30.0,
  "carb_pct": 40.0,
  "fat_pct": 30.0
}
```

### `FoodLog`
**Purpose**: Will validate food logging data
**Used By**: Future food logging endpoints

```python
class FoodLog(BaseModel):
    meal_type: str          # "breakfast", "lunch", "dinner", "snack"
    food_name: str          # Name of the food item
    calories: int           # Calorie content
    protein: float          # Protein in grams
    carbs: float            # Carbohydrates in grams
    fat: float              # Fat in grams
```

**Example**:
```json
{
  "meal_type": "breakfast",
  "food_name": "Oatmeal with berries",
  "calories": 300,
  "protein": 12.0,
  "carbs": 45.0,
  "fat": 8.0
}
```

### `AgentConsent`
**Purpose**: Will validate AI agent permission settings
**Used By**: Future agent management endpoints

```python
class AgentConsent(BaseModel):
    has_consented: bool     # Whether user consents to agent access
    agent_id: str           # Identifier for the AI agent
```

**Example**:
```json
{
  "has_consented": true,
  "agent_id": "meal-planner-v1"
}
```

---

## 🔍 Model Validation Rules

### Email Validation
- Uses `EmailStr` type for email fields
- Automatically validates email format
- Rejects invalid email addresses

### Optional Fields
- Fields marked as `Optional[str] = None` can be omitted
- If not provided, they default to `None`

### Type Validation
- `str`: Text strings
- `int`: Whole numbers
- `float`: Decimal numbers
- `bool`: True/false values
- `EmailStr`: Valid email addresses

---

## 📊 Database Mapping

| Model | Database Table | Purpose |
|-------|----------------|---------|
| `UserProfileCreate` | `user_profiles` | Create user profiles |
| `UserProfileResponse` | `user_profiles` | Return user profile data |
| `UserSignupRequest` | `auth.users` (future) | User registration |
| `UserLoginRequest` | `auth.users` (future) | User authentication |
| `MacroGoals` | `macro_preferences` (future) | Macro goal management |
| `FoodLog` | `food_logs` (future) | Food logging |
| `AgentConsent` | `agent_permissions` (future) | AI agent permissions | 