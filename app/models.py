from pydantic import BaseModel, EmailStr
from typing import Optional, List

# Authentication Models
# using models to validate the data that is sent to the API 
class UserSignupRequest(BaseModel):
    email: EmailStr
    password: str

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    message: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: str
    email: str

# User Profile Models
class UserProfileCreate(BaseModel):
    display_name: Optional[str] = None

class UserProfileResponse(BaseModel):
    user_id: str
    display_name: Optional[str]
    created_at: str
    updated_at: str

# Macro Goals Models
class MacroGoalsCreate(BaseModel):
    total_calories: int
    protein_pct: float
    carb_pct: float
    fat_pct: float

class MacroGoalsResponse(BaseModel):
    user_id: str
    total_calories: int
    protein_pct: float
    carb_pct: float
    fat_pct: float
    created_at: str
    updated_at: str

class MacroGoalsUpdate(BaseModel):
    total_calories: Optional[int] = None
    protein_pct: Optional[float] = None
    carb_pct: Optional[float] = None
    fat_pct: Optional[float] = None

# Food Logging Models (for later phases)
class FoodLogCreate(BaseModel):
    meal_type: str
    food_name: str
    calories: int
    protein: float
    carbs: float
    fat: float

class FoodLogResponse(BaseModel):
    id: str
    user_id: str
    meal_type: str
    food_name: str
    calories: int
    protein: float
    carbs: float
    fat: float
    logged_at: str
    created_at: str
    updated_at: str

class FoodLogUpdate(BaseModel):
    meal_type: Optional[str] = None
    food_name: Optional[str] = None
    calories: Optional[int] = None
    protein: Optional[float] = None
    carbs: Optional[float] = None
    fat: Optional[float] = None

# Food Summary Models
class MealSummary(BaseModel):
    meal_type: str
    calories: int
    protein: float
    carbs: float
    fat: float

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

class WeeklySummaryResponse(BaseModel):
    week_start: str
    week_end: str
    daily_averages: dict
    goal_averages: dict
    days_with_data: int
    total_days: int

# Email Models
class EmailRequest(BaseModel):
    to_email: EmailStr
    subject: str
    html_content: Optional[str] = None
    text_content: Optional[str] = None

class PasswordResetRequest(BaseModel):
    email: str

class PasswordResetResponse(BaseModel):
    message: str
    success: bool

class WelcomeEmailRequest(BaseModel):
    user_id: str
    email: EmailStr
    display_name: Optional[str] = None

class DailySummaryEmailRequest(BaseModel):
    user_id: str
    email: EmailStr
    date: str

class EmailResponse(BaseModel):
    message: str
    success: bool
    email_id: Optional[str] = None

# Agent Consent Models (for later phases)
class AgentConsent(BaseModel):
    has_consented: bool
    agent_id: str 