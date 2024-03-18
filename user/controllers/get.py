# user/controllers/get.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/{user_id}")
async def read_user(user_id: int):
  if user_id:
    return {"user_id": user_id}
  else:
    return {"users"}