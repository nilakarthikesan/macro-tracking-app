from fastapi import APIRouter, status, HTTPException, Depends
from backend.models import MacroGoalsCreate, MacroGoalsResponse, MacroGoalsUpdate
from backend.database import get_supabase
from backend.routers.auth import get_current_user

router = APIRouter(prefix="/macro-goals", tags=["macro goals"])

@router.post("/", response_model=MacroGoalsResponse, status_code=status.HTTP_201_CREATED)
async def create_macro_goals(
    goals_data: MacroGoalsCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Create or update macro goals for the current user.
    
    If the user already has goals, this will replace them.
    """
    try:
        supabase = get_supabase()
        user_id = current_user["user_id"]
        
        # Check if user already has goals
        existing_goals = supabase.table('macro_goals').select('*').eq('user_id', user_id).execute()
        
        if existing_goals.data:
            # Update existing goals
            response = supabase.table('macro_goals').update({
                'total_calories': goals_data.total_calories,
                'protein_pct': goals_data.protein_pct,
                'carb_pct': goals_data.carb_pct,
                'fat_pct': goals_data.fat_pct
            }).eq('user_id', user_id).execute()
        else:
            # Create new goals
            response = supabase.table('macro_goals').insert({
                'user_id': user_id,
                'total_calories': goals_data.total_calories,
                'protein_pct': goals_data.protein_pct,
                'carb_pct': goals_data.carb_pct,
                'fat_pct': goals_data.fat_pct
            }).execute()
        
        if response.data:
            goal = response.data[0]
            return MacroGoalsResponse(
                user_id=goal['user_id'],
                total_calories=goal['total_calories'],
                protein_pct=goal['protein_pct'],
                carb_pct=goal['carb_pct'],
                fat_pct=goal['fat_pct'],
                created_at=goal['created_at'],
                updated_at=goal['updated_at']
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create macro goals"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating macro goals: {str(e)}"
        )

@router.get("/", response_model=MacroGoalsResponse)
async def get_macro_goals(current_user: dict = Depends(get_current_user)):
    """
    Get the current user's macro goals.
    """
    try:
        supabase = get_supabase()
        user_id = current_user["user_id"]
        
        response = supabase.table('macro_goals').select('*').eq('user_id', user_id).execute()
        
        if response.data:
            goal = response.data[0]
            return MacroGoalsResponse(
                user_id=goal['user_id'],
                total_calories=goal['total_calories'],
                protein_pct=goal['protein_pct'],
                carb_pct=goal['carb_pct'],
                fat_pct=goal['fat_pct'],
                created_at=goal['created_at'],
                updated_at=goal['updated_at']
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No macro goals found for this user"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving macro goals: {str(e)}"
        )

@router.put("/", response_model=MacroGoalsResponse)
async def update_macro_goals(
    goals_data: MacroGoalsUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Update the current user's macro goals.
    Only provided fields will be updated.
    """
    try:
        supabase = get_supabase()
        user_id = current_user["user_id"]
        
        # Build update data with only provided fields
        update_data = {}
        if goals_data.total_calories is not None:
            update_data['total_calories'] = goals_data.total_calories
        if goals_data.protein_pct is not None:
            update_data['protein_pct'] = goals_data.protein_pct
        if goals_data.carb_pct is not None:
            update_data['carb_pct'] = goals_data.carb_pct
        if goals_data.fat_pct is not None:
            update_data['fat_pct'] = goals_data.fat_pct
        
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields provided for update"
            )
        
        response = supabase.table('macro_goals').update(update_data).eq('user_id', user_id).execute()
        
        if response.data:
            goal = response.data[0]
            return MacroGoalsResponse(
                user_id=goal['user_id'],
                total_calories=goal['total_calories'],
                protein_pct=goal['protein_pct'],
                carb_pct=goal['carb_pct'],
                fat_pct=goal['fat_pct'],
                created_at=goal['created_at'],
                updated_at=goal['updated_at']
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No macro goals found for this user"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating macro goals: {str(e)}"
        ) 