from fastapi import APIRouter, status, HTTPException, Depends
from app.models import FoodLogCreate, FoodLogResponse, FoodLogUpdate
from app.database import get_supabase
from app.routers.auth import get_current_user
from uuid import uuid4
from typing import List

router = APIRouter(prefix="/food-logs", tags=["food logs"])

@router.post("/", response_model=FoodLogResponse, status_code=status.HTTP_201_CREATED)
async def create_food_log(
    log_data: FoodLogCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Log a new food item for the current user.
    """
    try:
        supabase = get_supabase()
        user_id = current_user["user_id"]
        
        # Insert new food log
        response = supabase.table('food_logs').insert({
            'id': str(uuid4()),
            'user_id': user_id,
            'meal_type': log_data.meal_type,
            'food_name': log_data.food_name,
            'calories': log_data.calories,
            'protein': log_data.protein,
            'carbs': log_data.carbs,
            'fat': log_data.fat
        }).execute()
        
        if response.data:
            log = response.data[0]
            return FoodLogResponse(
                id=log['id'],
                user_id=log['user_id'],
                meal_type=log['meal_type'],
                food_name=log['food_name'],
                calories=log['calories'],
                protein=log['protein'],
                carbs=log['carbs'],
                fat=log['fat'],
                logged_at=log['logged_at'],
                created_at=log['created_at'],
                updated_at=log['updated_at']
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create food log"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating food log: {str(e)}"
        )

@router.get("/"