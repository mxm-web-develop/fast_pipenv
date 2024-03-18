# user/controllers/get.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_all_user_list():
  return {"users list [1,2,3,4,5,6]"}