from fastapi import APIRouter, Depends
from auth_guard import get_current_user

router = APIRouter(prefix="/protected", tags=["Protected"])

@router.get("/profile")
async def profile(user=Depends(get_current_user)):
    return {
        "id": user.id,
        "email": user.email,
        "created_at": str(user.created_at),
    }

@router.get("/dashboard")
async def dashboard(user=Depends(get_current_user)):
    return {
        "message": f"Welcome to your dashboard, {user.email}!",
        "user_id": user.id,
    }
