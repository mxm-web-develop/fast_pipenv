from fastapi import APIRouter, UploadFile, File, HTTPException
import fitz  # PyMuPDF
import io
from PIL import Image
import tempfile
import os
import hashlib
from pathlib import Path
import redis
import json

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
# 需要启动redis 在 6380
redis_client = redis.Redis(host='localhost', port=6380,db=0,decode_responses=True)

router = APIRouter()
PDF_EXTRACT_DIR = BASE_DIR / 'pdf_extract'
os.makedirs(BASE_DIR, exist_ok=True)

async def calculate_file_hash(file_content: bytes) -> str:
  sha256_hash = hashlib.sha256()
  sha256_hash.update(file_content)
  return sha256_hash.hexdigest()

@router.post("/pdf2img")
async def convert_pdf_to_images(file: UploadFile = File(...)):
    if file.content_type != 'application/pdf':
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF file.")

    content = await file.read()
    file_hash = await calculate_file_hash(content)
    redis_key = f"pdf:{file_hash}"

    # 从 Redis 获取数据
    if redis_client.exists(redis_key):
        data_json = redis_client.get(redis_key)
        return json.loads(data_json)  # 将 JSON 字符串转换回字典

    # 文件处理逻辑
    pdf_dir = PDF_EXTRACT_DIR / file_hash
    pdf_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = pdf_dir / file.filename

    with open(pdf_path, 'wb') as f:
        f.write(content)

    doc = fitz.open(pdf_path)
    pages_info = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        zoom_x, zoom_y = 2.0, 2.0  # 或根据需要调整以获得更好的质量
        mat = fitz.Matrix(zoom_x, zoom_y)
        pix = page.get_pixmap(matrix=mat)
        
        img = Image.open(io.BytesIO(pix.tobytes()))
        image_path = pdf_dir / f"page_{page_num + 1}.png"
        img.save(image_path)
        
        width, height = img.size
        pages_info.append({
            "url": str(image_path),
            "pageNum": page_num + 1,
            "modules": [],  # 添加其他所需信息
            "size": {"width": width, "height": height}
        })
    doc.close()

    data = {
        "filename": file.filename,
        "hash": file_hash,
        "status": 1,  # 假设 1 表示成功
        "pages": pages_info,
         "size": {"width": width, "height": height}
    }

    # 存储数据到 Redis
    data_json = json.dumps(data)
    redis_client.set(redis_key, data_json, ex=86400)  # 设置24小时过期

    return data