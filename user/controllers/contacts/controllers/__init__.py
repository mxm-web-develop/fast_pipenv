from fastapi import APIRouter
from .get_all import router as get_all_router
from .patch import router as patch_router

router = APIRouter()
router.include_router(get_all_router)
router.include_router(patch_router)