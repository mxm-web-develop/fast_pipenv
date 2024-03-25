from fastapi import APIRouter
from .pdf2img import router as pdf2img_router
from .cv import router as cv2img_router

router = APIRouter()
router.include_router(pdf2img_router)
router.include_router(cv2img_router)