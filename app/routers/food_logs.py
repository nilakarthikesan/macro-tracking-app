from fastapi import APIRouter, status, HTTPException, Depends
from app.models import FoodLogCreate, FoodLogResponse, FoodLogUpdate, DailySummaryResponse, WeeklySummaryResponse
from app.database import get_supabase
from app.routers.auth import get_current_user
from uuid import uuid4
from typing import List
from datetime import datetime, timedelta
import calendar

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

@router.get("/summary/daily", response_model=DailySummaryResponse)
async def get_daily_summary(
    date: str = None,
    current_user: dict = Depends(get_current_user)
):
    """
    Get daily macro summary for the current user.
    If no date is provided, uses today's date.
    """
    try:
        supabase = get_supabase()
        user_id = current_user["user_id"]
        
        # Use provided date or today's date
        if date is None:
            target_date = datetime.now().strftime("%Y-%m-%d")
        else:
            target_date = date
        
        # Get food logs for the specified date
        start_of_day = f"{target_date}T00:00:00"
        end_of_day = f"{target_date}T23:59:59"
        
        response = supabase.table('food_logs').select('*').eq('user_id', user_id).gte('logged_at', start_of_day).lte('logged_at', end_of_day).execute()
        
        # Calculate totals
        total_calories = 0
        total_protein = 0
        total_carbs = 0
        total_fat = 0
        meals = []
        
        if response.data:
            for log in response.data:
                total_calories += log['calories']
                total_protein += log['protein']
                total_carbs += log['carbs']
                total_fat += log['fat']
                
                meals.append({
                    'meal_type': log['meal_type'],
                    'calories': log['calories'],
                    'protein': log['protein'],
                    'carbs': log['carbs'],
                    'fat': log['fat']
                })
        
        # Get user's macro goals
        goals_response = supabase.table('macro_goals').select('*').eq('user_id', user_id).execute()
        
        if goals_response.data:
            goals = goals_response.data[0]
            goal_calories = goals['total_calories']
            goal_protein = (goals['protein_pct'] / 100) * goal_calories / 4  # Convert percentage to grams
            goal_carbs = (goals['carb_pct'] / 100) * goal_calories / 4
            goal_fat = (goals['fat_pct'] / 100) * goal_calories / 9
        else:
            # Default goals if none set
            goal_calories = 2000
            goal_protein = 150.0
            goal_carbs = 200.0
            goal_fat = 67.0
        
        # Calculate remaining macros
        calories_remaining = max(0, goal_calories - total_calories)
        protein_remaining = max(0, goal_protein - total_protein)
        carbs_remaining = max(0, goal_carbs - total_carbs)
        fat_remaining = max(0, goal_fat - total_fat)
        
        return DailySummaryResponse(
            date=target_date,
            total_calories=total_calories,
            total_protein=round(total_protein, 1),
            total_carbs=round(total_carbs, 1),
            total_fat=round(total_fat, 1),
            goal_calories=goal_calories,
            goal_protein=round(goal_protein, 1),
            goal_carbs=round(goal_carbs, 1),
            goal_fat=round(goal_fat, 1),
            calories_remaining=calories_remaining,
            protein_remaining=round(protein_remaining, 1),
            carbs_remaining=round(carbs_remaining, 1),
            fat_remaining=round(fat_remaining, 1),
            meals=meals
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting daily summary: {str(e)}"
        )

@router.get("/summary/weekly", response_model=WeeklySummaryResponse)
async def get_weekly_summary(
    week_start: str = None,
    current_user: dict = Depends(get_current_user)
):
    """
    Get weekly macro summary for the current user.
    If no week_start is provided, uses the current week.
    """
    try:
        supabase = get_supabase()
        user_id = current_user["user_id"]
        
        # Calculate week start and end dates
        if week_start is None:
            today = datetime.now()
            week_start_date = today - timedelta(days=today.weekday())
            week_start = week_start_date.strftime("%Y-%m-%d")
        
        week_start_date = datetime.strptime(week_start, "%Y-%m-%d")
        week_end_date = week_start_date + timedelta(days=6)
        week_end = week_end_date.strftime("%Y-%m-%d")
        
        # Get food logs for the week
        start_of_week = f"{week_start}T00:00:00"
        end_of_week = f"{week_end}T23:59:59"
        
        response = supabase.table('food_logs').select('*').eq('user_id', user_id).gte('logged_at', start_of_week).lte('logged_at', end_of_week).execute()
        
        # Calculate daily totals
        daily_totals = {}
        days_with_data = set()
        
        if response.data:
            for log in response.data:
                log_date = log['logged_at'][:10]  # Extract date part
                days_with_data.add(log_date)
                
                if log_date not in daily_totals:
                    daily_totals[log_date] = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}
                
                daily_totals[log_date]['calories'] += log['calories']
                daily_totals[log_date]['protein'] += log['protein']
                daily_totals[log_date]['carbs'] += log['carbs']
                daily_totals[log_date]['fat'] += log['fat']
        
        # Calculate averages
        if daily_totals:
            total_calories = sum(day['calories'] for day in daily_totals.values())
            total_protein = sum(day['protein'] for day in daily_totals.values())
            total_carbs = sum(day['carbs'] for day in daily_totals.values())
            total_fat = sum(day['fat'] for day in daily_totals.values())
            
            num_days = len(daily_totals)
            
            daily_averages = {
                'calories': round(total_calories / num_days),
                'protein': round(total_protein / num_days, 1),
                'carbs': round(total_carbs / num_days, 1),
                'fat': round(total_fat / num_days, 1)
            }
        else:
            daily_averages = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}
        
        # Get user's macro goals
        goals_response = supabase.table('macro_goals').select('*').eq('user_id', user_id).execute()
        
        if goals_response.data:
            goals = goals_response.data[0]
            goal_calories = goals['total_calories']
            goal_protein = (goals['protein_pct'] / 100) * goal_calories / 4
            goal_carbs = (goals['carb_pct'] / 100) * goal_calories / 4
            goal_fat = (goals['fat_pct'] / 100) * goal_calories / 9
        else:
            # Default goals if none set
            goal_calories = 2000
            goal_protein = 150.0
            goal_carbs = 200.0
            goal_fat = 67.0
        
        goal_averages = {
            'calories': goal_calories,
            'protein': round(goal_protein, 1),
            'carbs': round(goal_carbs, 1),
            'fat': round(goal_fat, 1)
        }
        
        return WeeklySummaryResponse(
            week_start=week_start,
            week_end=week_end,
            daily_averages=daily_averages,
            goal_averages=goal_averages,
            days_with_data=len(days_with_data),
            total_days=7
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting weekly summary: {str(e)}"
        ) 