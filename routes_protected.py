from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(prefix="/protected", tags=["Protected"])
security = HTTPBearer()

@router.get("/profile")
async def profile(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if not token:
        raise HTTPException(status_code=401, detail="Access token required")
    # Not returning user info yet as it's not verified
    return {"message": "Token presented but not verified yet"}
