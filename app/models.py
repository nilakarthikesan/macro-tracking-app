from pydantic import BaseModel, EmailStr
from typing import Optional

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

# Agent Consent Models (for later phases)
class AgentConsent(BaseModel):
    has_consented: bool
    agent_id: str 