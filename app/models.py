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
    user_id: str
    display_name: Optional[str] = None

class UserProfileResponse(BaseModel):
    user_id: str
    display_name: Optional[str]
    created_at: str
    updated_at: str

# Future Models (for later phases)
# These will be used when we add macro tracking and food logging

class MacroGoals(BaseModel):
    total_calories: int
    protein_pct: float
    carb_pct: float
    fat_pct: float

class FoodLog(BaseModel):
    meal_type: str
    food_name: str
    calories: int
    protein: float
    carbs: float
    fat: float

class AgentConsent(BaseModel):
    has_consented: bool
    agent_id: str 