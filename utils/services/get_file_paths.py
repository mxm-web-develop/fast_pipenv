import redis
import json
from typing import List, Optional
from pathlib import Path
import os

# 初始化 Redis 客户端
redis_client = redis.Redis(host='localhost', port=6380, db=0, decode_responses=True)

def get_file_paths(hash: str, pageNum: Optional[int] = None) -> List[str]:
    redis_key = f"pdf:{hash}"
    if not redis_client.exists(redis_key):
        return []  # 如果文件不存在，返回空列表

    # 从 Redis 获取数据
    data_json = redis_client.get(redis_key)
    data = json.loads(data_json)
    print('data',data)
    # 获取基础目录
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    PDF_EXTRACT_DIR = BASE_DIR / 'pdf_extract'

    # 如果指定了 pageNum，则只返回该页面的路径
    if pageNum is not None:
        if 1 <= pageNum <= len(data['pages']):
            page_info = data['pages'][pageNum - 1]
            # 构造文件的完整路径
            file_path = str(PDF_EXTRACT_DIR / hash / Path(page_info['url']).name)
            return [file_path]  # 返回单页的路径列表
        else:
            return []  # 如果页面编号不在范围内，返回空列表
    # 否则，返回所有页面的路径
    else:
        print( [str(PDF_EXTRACT_DIR / hash / Path(page['url']).name) for page in data['pages']])
        return [str(PDF_EXTRACT_DIR / hash / Path(page['url']).name) for page in data['pages']]