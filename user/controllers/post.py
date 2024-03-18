from fastapi import APIRouter, HTTPException, Body
from user.services import create_user_by_email

router = APIRouter()

@router.post("/")
async def create_user(email: str = Body(...), name: str = Body(...)):
    # 使用服务层的功能
    user = create_user_by_email(email, name)
    if user:
        return user
    raise HTTPException(status_code=400, detail="Could not create user.")
