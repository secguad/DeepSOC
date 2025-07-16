import pytest
import os
from app.services.file_analyzer import FileAnalyzer
from app.core.config import settings

@pytest.mark.asyncio
async def test_image_ocr():
    """测试图片OCR功能"""
    analyzer = FileAnalyzer()
    
    # 创建一个测试图片
    test_image_path = "tests/test_data/test_image.png"
    os.makedirs(os.path.dirname(test_image_path), exist_ok=True)
    
    # 使用OpenCV创建一个测试图片
    import cv2
    import numpy as np
    
    # 创建一个白色背景的图片
    img = np.ones((200, 400), dtype=np.uint8) * 255
    
    # 添加一些文字
    cv2.putText(img, "测试文本", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, 0, 2)
    cv2.putText(img, "Test Text", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, 0, 2)
    
    # 保存图片
    cv2.imwrite(test_image_path, img)
    
    # 分析图片
    result = await analyzer.analyze_file(f"file://{os.path.abspath(test_image_path)}")
    
    # 验证结果
    assert result["success"] is True
    assert len(result["results"]) > 0
    assert "测试文本" in result["results"][0]["content"]
    assert "Test Text" in result["results"][0]["content"]
    
    # 清理测试文件
    os.remove(test_image_path)

@pytest.mark.asyncio
async def test_excel_analysis():
    """测试Excel文件分析功能"""
    analyzer = FileAnalyzer()
    
    # 创建一个测试Excel文件
    test_excel_path = "tests/test_data/test_data.xlsx"
    os.makedirs(os.path.dirname(test_excel_path), exist_ok=True)
    
    # 使用pandas创建测试数据
    import pandas as pd
    
    data = {
        "姓名": ["张三", "李四", "王五"],
        "手机号": ["13800138000", "13900139000", "13700137000"],
        "身份证号": ["110101199001011234", "110101199001011235", "110101199001011236"]
    }
    
    df = pd.DataFrame(data)
    df.to_excel(test_excel_path, index=False)
    
    # 分析Excel文件
    result = await analyzer.analyze_file(f"file://{os.path.abspath(test_excel_path)}")
    
    # 验证结果
    assert result["success"] is True
    assert len(result["results"]) > 0
    assert "姓名" in result["results"][0]["columns"]
    assert "手机号" in result["results"][0]["columns"]
    assert "身份证号" in result["results"][0]["columns"]
    
    # 清理测试文件
    os.remove(test_excel_path)

@pytest.mark.asyncio
async def test_archive_analysis():
    """测试压缩文件分析功能"""
    analyzer = FileAnalyzer()
    
    # 创建测试目录
    test_dir = "tests/test_data/test_archive"
    os.makedirs(test_dir, exist_ok=True)
    
    # 创建测试文件
    test_files = {
        "test1.txt": "测试文本1",
        "test2.txt": "测试文本2",
        "test3.xlsx": pd.DataFrame({"测试列": ["测试数据"]})
    }
    
    for filename, content in test_files.items():
        filepath = os.path.join(test_dir, filename)
        if isinstance(content, str):
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
        else:
            content.to_excel(filepath, index=False)
    
    # 创建ZIP文件
    import zipfile
    test_zip_path = "tests/test_data/test_archive.zip"
    with zipfile.ZipFile(test_zip_path, "w") as zipf:
        for root, _, files in os.walk(test_dir):
            for file in files:
                filepath = os.path.join(root, file)
                arcname = os.path.relpath(filepath, test_dir)
                zipf.write(filepath, arcname)
    
    # 分析ZIP文件
    result = await analyzer.analyze_file(f"file://{os.path.abspath(test_zip_path)}")
    
    # 验证结果
    assert result["success"] is True
    assert len(result["results"]) > 0
    
    # 清理测试文件
    import shutil
    shutil.rmtree(test_dir)
    os.remove(test_zip_path)

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 