# user/controllers/get.py
from fastapi import APIRouter

from contacts.services import update_by_email

router = APIRouter()

@router.get("/{email}")
async def update_contact():
  result =update_by_email()
  return result