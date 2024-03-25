import cv2
import numpy as np
from pathlib import Path
from typing import List, Dict, Any ,Tuple
import easyocr

# 初始化EasyOCR reader
reader = easyocr.Reader(['en'], gpu=True)  # 'en' 是语言代码

def preprocess_image(image_path: str) -> List[Dict[str, Any]]:
    if not Path(image_path).is_file():
        raise FileNotFoundError(f"The image file does not exist: {image_path}")

    # 读取图像
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Could not read the image file: {image_path}")

    # 转换为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 二值化
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    # 使用膨胀和腐蚀操作改善文本区域
    kernel = np.ones((5, 5), np.uint8)
    dilation = cv2.dilate(binary, kernel, iterations=1)
    erosion = cv2.erode(dilation, kernel, iterations=1)

    # 寻找轮廓
    contours, _ = cv2.findContours(erosion, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    modules = []  # 用于存储每个识别的块信息
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w > 30 and h > 30:
            position = [[x, y], [x + w, y + h]]
            modules.append({
                "type": "unknown",
                "position": position,
            })

    # 使用OCR更新modules中的文本区域信息
    # modules = detect_text_area(image_path, modules)
    return modules

def detect_text_area(image_path: str, modules: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    image = cv2.imread(image_path)

    results = reader.readtext(image, detail=1, paragraph=False)
    for result in results:
        bbox, text, _ = result  # OCR结果中的位置信息和文本
        x_min, y_min = [int(val) for val in bbox[0]]
        x_max, y_max = [int(val) for val in bbox[2]]

        for module in modules:
            if module['type'] == 'unknown' and module_in_range((x_min, y_min, x_max, y_max), module['position']):
                module['type'] = 'text'
                module['content'] = text

    return modules

def module_in_range(ocr_bbox: Tuple[int, int, int, int], module_position: List[List[int]]) -> bool:
    ocr_x_min, ocr_y_min, ocr_x_max, ocr_y_max = ocr_bbox
    mod_x_min, mod_y_min = module_position[0]
    mod_x_max, mod_y_max = module_position[1]

    # 简化的检查：如果OCR边界框与模块边界框有重叠，则认为文本属于该模块
    return not (ocr_x_max < mod_x_min or ocr_x_min > mod_x_max or
                ocr_y_max < mod_y_min or ocr_y_min > mod_y_max)
