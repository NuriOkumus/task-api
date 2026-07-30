from fastapi import APIRouter, HTTPException, Depends, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from supabase_client import supabase
from auth_guard import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


class AuthBody(BaseModel):
    email: str = ""
    password: str = ""


@router.post("/signup")
async def signup(body: AuthBody):
    if not body.email or not body.password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    try:
        result = supabase.auth.sign_up({"email": body.email, "password": body.password})

        if result.user is None:
            raise HTTPException(status_code=400, detail="Signup failed")

        return JSONResponse(status_code=201, content={
            "user": {
                "id": result.user.id,
                "email": result.user.email,
                "created_at": str(result.user.created_at),
            }
        })
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def login(body: AuthBody):
    if not body.email or not body.password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    try:
        result = supabase.auth.sign_in_with_password({"email": body.email, "password": body.password})

        return {
            "access_token": result.session.access_token,
            "refresh_token": result.session.refresh_token,
            "token_type": "bearer",
        }
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid login credentials")


@router.post("/logout")
async def logout(user=Depends(get_current_user)):
    try:
        supabase.auth.sign_out()
        return Response(status_code=204)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
