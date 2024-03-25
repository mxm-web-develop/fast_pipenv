from fastapi import APIRouter
from .post import router as cv_router

router = APIRouter()
router.include_router(cv_router)