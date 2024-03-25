from fastapi import APIRouter, UploadFile, File, HTTPException
from utils.services.cv_from_img import preprocess_image
from utils.services.get_file_paths import get_file_paths

router = APIRouter()

@router.post("/cv")
async def api_get_file_paths(hash: str, pageNum: int ):
    # 从 Redis 获取对应的单个页面文件路径
    paths = get_file_paths(hash, pageNum)
    if not paths:
        raise HTTPException(status_code=404, detail="File not found or page number out of range.")
    
    # 对指定页进行预处理
    page_path = paths[0]  # 取得单页路径
    res = preprocess_image(page_path)  # 调用图像处理函数
    print("Processing result:", res) 
    # 返回预处理结果
        # 确保 res 是可序列化的格式，例如：
    response_data = {
        "message": "Image processed successfully",
        "result": res  # 这里改为一个简单的字符串，以测试响应结构
    }
    return response_data