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

@router.get("/", response_model=List[FoodLogResponse])
async def get_food_logs(current_user: dict = Depends(get_current_user)):
    """
    Get all food logs for the current user.
    """
    try:
        supabase = get_supabase()
        user_id = current_user["user_id"]
        
        response = supabase.table('food_logs').select('*').eq('user_id', user_id).order('logged_at', desc=True).execute()
        
        if response.data:
            return [
                FoodLogResponse(
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
                for log in response.data
            ]
        else:
            return []
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving food logs: {str(e)}"
        )

@router.put("/{log_id}", response_model=FoodLogResponse)
async def update_food_log(
    log_id: str,
    log_data: FoodLogUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Update a food log entry for the current user.
    """
    try:
        supabase = get_supabase()
        user_id = current_user["user_id"]
        
        # Build update data with only provided fields
        update_data = {}
        if log_data.meal_type is not None:
            update_data['meal_type'] = log_data.meal_type
        if log_data.food_name is not None:
            update_data['food_name'] = log_data.food_name
        if log_data.calories is not None:
            update_data['calories'] = log_data.calories
        if log_data.protein is not None:
            update_data['protein'] = log_data.protein
        if log_data.carbs is not None:
            update_data['carbs'] = log_data.carbs
        if log_data.fat is not None:
            update_data['fat'] = log_data.fat
        
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields provided for update"
            )
        
        response = supabase.table('food_logs').update(update_data).eq('id', log_id).eq('user_id', user_id).execute()
        
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
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Food log not found or you don't have permission to update it"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating food log: {str(e)}"
        )

@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_food_log(
    log_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Delete a food log entry for the current user.
    """
    try:
        supabase = get_supabase()
        user_id = current_user["user_id"]
        
        response = supabase.table('food_logs').delete().eq('id', log_id).eq('user_id', user_id).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Food log not found or you don't have permission to delete it"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting food log: {str(e)}"
        ) 