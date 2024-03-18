from fastapi import APIRouter

router = APIRouter()

@router.delete("/{user_id}")
async def delete_user(user_id: int):
  if user_id:
    return {"user_id": user_id}
  else:
    return {"users"}