# Pydantic Models Documentation

## Overview
This document describes all the Pydantic models used in the Macro Tracking App for request/response validation and data serialization.

---

## Authentication Models

### UserSignupRequest
**Purpose**: User registration request data
**Used in**: `POST /auth/signup`

```python
class UserSignupRequest(BaseModel):
    email: str
    password: str
```

**Validation Rules**:
- `email`: Must be a valid email format
- `password`: Must be a non-empty string

### UserLoginRequest
**Purpose**: User login request data
**Used in**: `POST /auth/login`

```python
class UserLoginRequest(BaseModel):
    email: str
    password: str
```

**Validation Rules**:
- `email`: Must be a valid email format
- `password`: Must be a non-empty string

### TokenResponse
**Purpose**: Authentication token response
**Used in**: `POST /auth/signup`, `POST /auth/login`

```python
class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: str
    email: str
```

**Fields**:
- `access_token`: JWT token for authentication
- `token_type`: Always "bearer"
- `user_id`: User's unique identifier
- `email`: User's email address

### UserResponse
**Purpose**: User information response
**Used in**: `GET /auth/me`

```python
class UserResponse(BaseModel):
    id: str
    email: str
    message: str
```

**Fields**:
- `id`: User's unique identifier
- `email`: User's email address
- `message`: Additional information about the response

### PasswordResetRequest
**Purpose**: Password reset request data
**Used in**: `POST /auth/password-reset`

```python
class PasswordResetRequest(BaseModel):
    email: str
```

**Validation Rules**:
- `email`: Must be a valid email format

---

## Profile Models

### ProfileCreate
**Purpose**: User profile creation request
**Used in**: `POST /profiles/`

```python
class ProfileCreate(BaseModel):
    display_name: str
```

**Validation Rules**:
- `display_name`: Must be a non-empty string

### ProfileResponse
**Purpose**: User profile response data
**Used in**: `POST /profiles/`

```python
class ProfileResponse(BaseModel):
    user_id: str
    display_name: str
    created_at: datetime
    updated_at: datetime
```

**Fields**:
- `user_id`: User's unique identifier
- `display_name`: User's display name
- `created_at`: Profile creation timestamp
- `updated_at`: Last update timestamp

---

## Macro Goals Models

### MacroGoalsCreate
**Purpose**: Macro goals creation/update request
**Used in**: `POST /macro-goals/`

```python
class MacroGoalsCreate(BaseModel):
    total_calories: int
    protein_pct: float
    carb_pct: float
    fat_pct: float
```

**Validation Rules**:
- `total_calories`: Must be a positive integer
- `protein_pct`: Must be between 0 and 100
- `carb_pct`: Must be between 0 and 100
- `fat_pct`: Must be between 0 and 100
- Total percentages must equal 100%

### MacroGoalsUpdate
**Purpose**: Macro goals partial update request
**Used in**: `PUT /macro-goals/`

```python
class MacroGoalsUpdate(BaseModel):
    total_calories: Optional[int] = None
    protein_pct: Optional[float] = None
    carb_pct: Optional[float] = None
    fat_pct: Optional[float] = None
```

**Validation Rules**:
- All fields are optional
- If provided, must follow same rules as MacroGoalsCreate
- If all percentages are provided, must equal 100%

### MacroGoalsResponse
**Purpose**: Macro goals response data
**Used in**: `GET /macro-goals/`, `POST /macro-goals/`, `PUT /macro-goals/`

```python
class MacroGoalsResponse(BaseModel):
    user_id: str
    total_calories: int
    protein_pct: float
    carb_pct: float
    fat_pct: float
    created_at: datetime
    updated_at: datetime
```

**Fields**:
- `user_id`: User's unique identifier
- `total_calories`: Daily calorie target
- `protein_pct`: Protein percentage target
- `carb_pct`: Carbohydrate percentage target
- `fat_pct`: Fat percentage target
- `created_at`: Goals creation timestamp
- `updated_at`: Last update timestamp

---

## Food Logging Models

### FoodLogCreate
**Purpose**: Food log creation request
**Used in**: `POST /food-logs/`

```python
class FoodLogCreate(BaseModel):
    meal_type: str
    food_name: str
    calories: int
    protein: float
    carbs: float
    fat: float
```

**Validation Rules**:
- `meal_type`: Must be one of: "breakfast", "lunch", "dinner", "snack"
- `food_name`: Must be a non-empty string
- `calories`: Must be a non-negative integer
- `protein`: Must be a non-negative float
- `carbs`: Must be a non-negative float
- `fat`: Must be a non-negative float

### FoodLogUpdate
**Purpose**: Food log partial update request
**Used in**: `PUT /food-logs/{log_id}`

```python
class FoodLogUpdate(BaseModel):
    meal_type: Optional[str] = None
    food_name: Optional[str] = None
    calories: Optional[int] = None
    protein: Optional[float] = None
    carbs: Optional[float] = None
    fat: Optional[float] = None
```

**Validation Rules**:
- All fields are optional
- If provided, must follow same rules as FoodLogCreate

### FoodLogResponse
**Purpose**: Food log response data
**Used in**: `GET /food-logs/`, `POST /food-logs/`, `PUT /food-logs/{log_id}`

```python
class FoodLogResponse(BaseModel):
    id: str
    user_id: str
    meal_type: str
    food_name: str
    calories: int
    protein: float
    carbs: float
    fat: float
    logged_at: datetime
    created_at: datetime
    updated_at: datetime
```

**Fields**:
- `id`: Food log unique identifier
- `user_id`: User's unique identifier
- `meal_type`: Type of meal
- `food_name`: Name of the food item
- `calories`: Calorie content
- `protein`: Protein content in grams
- `carbs`: Carbohydrate content in grams
- `fat`: Fat content in grams
- `logged_at`: When the food was logged
- `created_at`: Log creation timestamp
- `updated_at`: Last update timestamp

---

## Summary Models

### DailySummaryResponse
**Purpose**: Daily macro summary response
**Used in**: `GET /food-logs/summary/daily`

```python
class DailySummaryResponse(BaseModel):
    date: str
    total_calories: int
    total_protein: float
    total_carbs: float
    total_fat: float
    goal_calories: int
    goal_protein: float
    goal_carbs: float
    goal_fat: float
    calories_remaining: int
    protein_remaining: float
    carbs_remaining: float
    fat_remaining: float
    meals: List[MealSummary]
```

**Fields**:
- `date`: Date in YYYY-MM-DD format
- `total_calories`: Total calories consumed
- `total_protein`: Total protein consumed in grams
- `total_carbs`: Total carbs consumed in grams
- `total_fat`: Total fat consumed in grams
- `goal_calories`: Daily calorie goal
- `goal_protein`: Daily protein goal in grams
- `goal_carbs`: Daily carb goal in grams
- `goal_fat`: Daily fat goal in grams
- `calories_remaining`: Remaining calories for the day
- `protein_remaining`: Remaining protein for the day
- `carbs_remaining`: Remaining carbs for the day
- `fat_remaining`: Remaining fat for the day
- `meals`: List of meals with their macro totals

### MealSummary
**Purpose**: Individual meal summary data
**Used in**: DailySummaryResponse

```python
class MealSummary(BaseModel):
    meal_type: str
    calories: int
    protein: float
    carbs: float
    fat: float
```

**Fields**:
- `meal_type`: Type of meal (breakfast, lunch, dinner, snack)
- `calories`: Total calories for this meal type
- `protein`: Total protein for this meal type
- `carbs`: Total carbs for this meal type
- `fat`: Total fat for this meal type

### WeeklySummaryResponse
**Purpose**: Weekly macro summary response
**Used in**: `GET /food-logs/summary/weekly`

```python
class WeeklySummaryResponse(BaseModel):
    week_start: str
    week_end: str
    total_calories: int
    total_protein: float
    total_carbs: float
    total_fat: float
    daily_averages: DailyAverages
    goal_calories: int
    goal_protein: float
    goal_carbs: float
    goal_fat: float
    daily_totals: Dict[str, DailyTotals]
```

**Fields**:
- `week_start`: Start of week in YYYY-MM-DD format
- `week_end`: End of week in YYYY-MM-DD format
- `total_calories`: Total calories for the week
- `total_protein`: Total protein for the week
- `total_carbs`: Total carbs for the week
- `total_fat`: Total fat for the week
- `daily_averages`: Average daily macros
- `goal_calories`: Daily calorie goal
- `goal_protein`: Daily protein goal
- `goal_carbs`: Daily carb goal
- `goal_fat`: Daily fat goal
- `daily_totals`: Daily totals for each day of the week

### DailyAverages
**Purpose**: Daily average macro calculations
**Used in**: WeeklySummaryResponse

```python
class DailyAverages(BaseModel):
    calories: float
    protein: float
    carbs: float
    fat: float
```

**Fields**:
- `calories`: Average daily calories
- `protein`: Average daily protein
- `carbs`: Average daily carbs
- `fat`: Average daily fat

### DailyTotals
**Purpose**: Daily macro totals
**Used in**: WeeklySummaryResponse

```python
class DailyTotals(BaseModel):
    calories: int
    protein: float
    carbs: float
    fat: float
```

**Fields**:
- `calories`: Total calories for the day
- `protein`: Total protein for the day
- `carbs`: Total carbs for the day
- `fat`: Total fat for the day

---

## Model Validation Rules

### Email Validation
- Must be a valid email format
- Uses Pydantic's built-in email validator

### Percentage Validation
- Must be between 0 and 100
- Total percentages must equal 100% for macro goals

### Numeric Validation
- Calories: Non-negative integers
- Macros (protein, carbs, fat): Non-negative floats
- Percentages: Floats between 0 and 100

### String Validation
- Non-empty strings for required text fields
- Meal types must be from predefined list

### Date/Time Validation
- Uses Pydantic's datetime validation
- Dates formatted as YYYY-MM-DD strings
- Timestamps in ISO format

### UUID Validation
- Uses Pydantic's UUID validation
- Automatically validates UUID format

---

## Error Response Models

### ErrorResponse
**Purpose**: Standard error response format
**Used in**: All error responses

```python
class ErrorResponse(BaseModel):
    detail: str
```

**Fields**:
- `detail`: Error message describing what went wrong

### ValidationError
**Purpose**: Pydantic validation error response
**Used in**: Automatic validation errors

```python
class ValidationError(BaseModel):
    loc: List[Union[str, int]]
    msg: str
    type: str
```

**Fields**:
- `loc`: Location of the error in the request
- `msg`: Error message
- `type`: Type of validation error

---

## Usage Examples

### Creating a Food Log
```python
# Request
food_log = FoodLogCreate(
    meal_type="breakfast",
    food_name="Oatmeal with berries",
    calories=250,
    protein=8.5,
    carbs=45.2,
    fat=4.1
)

# Response
response = FoodLogResponse(
    id="da31eb61-6ec3-400f-b36e-cb83807c71e",
    user_id="b7bcb761-e36b-4f65-ae62-da2451005f32",
    meal_type="breakfast",
    food_name="Oatmeal with berries",
    calories=250,
    protein=8.5,
    carbs=45.2,
    fat=4.1,
    logged_at=datetime.now(),
    created_at=datetime.now(),
    updated_at=datetime.now()
)
```

### Setting Macro Goals
```python
# Request
goals = MacroGoalsCreate(
    total_calories=2000,
    protein_pct=30.0,
    carb_pct=40.0,
    fat_pct=30.0
)

# Response
response = MacroGoalsResponse(
    user_id="b7bcb761-e36b-4f65-ae62-da2451005f32",
    total_calories=2000,
    protein_pct=30.0,
    carb_pct=40.0,
    fat_pct=30.0,
    created_at=datetime.now(),
    updated_at=datetime.now()
)
```

---

## Best Practices

1. **Always validate input**: Use Pydantic models for all request/response data
2. **Provide clear error messages**: Use descriptive validation rules
3. **Use appropriate data types**: Choose the right types for your data
4. **Document your models**: Keep this documentation updated
5. **Test validation rules**: Ensure all validation works as expected
6. **Use consistent naming**: Follow consistent naming conventions
7. **Handle optional fields**: Use Optional types for partial updates
8. **Validate business rules**: Add custom validators for complex rules 