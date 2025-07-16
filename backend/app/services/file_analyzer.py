import logging
import aiohttp
import pandas as pd
import io
import zipfile
import rarfile
import os
import platform
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from app.core.config import settings
import pytesseract
from PIL import Image
import cv2
import numpy as np

logger = logging.getLogger(__name__)

class FileAnalyzer:
    def __init__(self):
        self.temp_dir = "temp"
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
        
        # 设置Tesseract路径
        pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD
        
        # 初始化OCR配置
        self.tesseract_config = '--oem 3 --psm 6 -l chi_sim+chi_tra+eng'
        
        # 支持的图片格式
        self.image_extensions = ['jpg', 'jpeg', 'png', 'bmp', 'tiff']
        
        # 支持的文档格式
        self.document_extensions = ['xlsx', 'xls', 'csv']
        
        # 支持的压缩格式
        self.archive_extensions = ['zip', 'rar', '7z']
        
        # 检查Tesseract是否可用
        self._check_tesseract()
        
        # 检查系统环境
        self._check_system_environment()

    def _check_tesseract(self):
        """检查Tesseract是否可用"""
        try:
            pytesseract.get_tesseract_version()
        except Exception as e:
            logger.error(f"Tesseract检查失败: {str(e)}")
            logger.error("请确保已安装Tesseract并设置正确的路径")
            logger.error("Windows: 安装Tesseract-OCR并设置环境变量")
            logger.error("Linux: sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim tesseract-ocr-chi-tra")
            logger.error("macOS: brew install tesseract tesseract-lang")
            raise

    def _check_system_environment(self):
        """检查系统环境"""
        system = platform.system().lower()
        if system == 'windows':
            # Windows特定检查
            if not os.path.exists(settings.TESSERACT_CMD):
                logger.error(f"Tesseract未找到: {settings.TESSERACT_CMD}")
                logger.error("请安装Tesseract-OCR并设置正确的路径")
                raise FileNotFoundError(f"Tesseract未找到: {settings.TESSERACT_CMD}")
        elif system == 'linux':
            # Linux特定检查
            try:
                import subprocess
                subprocess.run(['tesseract', '--version'], capture_output=True, check=True)
            except subprocess.CalledProcessError:
                logger.error("Tesseract未安装或未正确配置")
                raise
        elif system == 'darwin':
            # macOS特定检查
            try:
                import subprocess
                subprocess.run(['tesseract', '--version'], capture_output=True, check=True)
            except subprocess.CalledProcessError:
                logger.error("Tesseract未安装或未正确配置")
                raise

    async def download_file(self, url: str) -> Optional[str]:
        """下载文件"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        # 生成临时文件名
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        file_extension = url.split('.')[-1].lower()
                        temp_file = os.path.join(self.temp_dir, f"temp_{timestamp}.{file_extension}")
                        
                        # 保存文件
                        with open(temp_file, 'wb') as f:
                            f.write(await response.read())
                        return temp_file
                    else:
                        logger.error(f"下载文件失败: {response.status}")
                        return None
        except Exception as e:
            logger.error(f"下载文件出错: {str(e)}")
            return None

    def preprocess_image(self, image_path: str) -> Optional[np.ndarray]:
        """图像预处理，提高OCR识别率"""
        try:
            # 读取图像
            image = cv2.imread(image_path)
            if image is None:
                return None
            
            # 转换为灰度图
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # 自适应阈值处理
            binary = cv2.adaptiveThreshold(
                gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                cv2.THRESH_BINARY, 11, 2
            )
            
            # 降噪
            denoised = cv2.fastNlMeansDenoising(binary)
            
            # 锐化
            kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
            sharpened = cv2.filter2D(denoised, -1, kernel)
            
            return sharpened
        except Exception as e:
            logger.error(f"图像预处理失败: {str(e)}")
            return None

    def perform_ocr(self, image_path: str) -> Tuple[bool, str]:
        """执行OCR识别"""
        try:
            # 预处理图像
            processed_image = self.preprocess_image(image_path)
            if processed_image is None:
                return False, "图像预处理失败"
            
            # 保存处理后的图像
            temp_processed = os.path.join(self.temp_dir, "processed_" + os.path.basename(image_path))
            cv2.imwrite(temp_processed, processed_image)
            
            # 执行OCR
            text = pytesseract.image_to_string(
                Image.open(temp_processed),
                config=self.tesseract_config
            )
            
            # 清理临时文件
            try:
                os.remove(temp_processed)
            except Exception as e:
                logger.warning(f"清理临时文件失败: {str(e)}")
            
            return True, text.strip()
        except Exception as e:
            logger.error(f"OCR识别失败: {str(e)}")
            return False, str(e)

    def extract_archive(self, file_path: str) -> List[str]:
        """解压压缩文件"""
        extracted_files = []
        try:
            if file_path.endswith('.zip'):
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(self.temp_dir)
                    extracted_files = [os.path.join(self.temp_dir, f) for f in zip_ref.namelist()]
            elif file_path.endswith('.rar'):
                with rarfile.RarFile(file_path, 'r') as rar_ref:
                    rar_ref.extractall(self.temp_dir)
                    extracted_files = [os.path.join(self.temp_dir, f) for f in rar_ref.namelist()]
            return extracted_files
        except Exception as e:
            logger.error(f"解压文件出错: {str(e)}")
            return []

    def read_excel_content(self, file_path: str) -> Tuple[bool, str, List[str]]:
        """读取Excel文件内容"""
        try:
            # 读取Excel文件
            df = pd.read_excel(file_path)
            
            # 获取列名
            columns = df.columns.tolist()
            
            # 获取前几行数据作为样本
            sample_data = df.head(5).to_string()
            
            return True, sample_data, columns
        except Exception as e:
            logger.error(f"读取Excel文件出错: {str(e)}")
            return False, "", []

    def read_csv_content(self, file_path: str) -> Tuple[bool, str, List[str]]:
        """读取CSV文件内容"""
        try:
            # 读取CSV文件
            df = pd.read_csv(file_path)
            
            # 获取列名
            columns = df.columns.tolist()
            
            # 获取前几行数据作为样本
            sample_data = df.head(5).to_string()
            
            return True, sample_data, columns
        except Exception as e:
            logger.error(f"读取CSV文件出错: {str(e)}")
            return False, "", []

    def analyze_image_content(self, file_path: str) -> Dict:
        """分析图片内容"""
        try:
            # 执行OCR识别
            success, text = self.perform_ocr(file_path)
            
            if not success:
                return {
                    "success": False,
                    "error": text
                }
            
            return {
                "success": True,
                "content": text,
                "file_type": "image",
                "columns": []  # 图片没有列名
            }
            
        except Exception as e:
            logger.error(f"分析图片内容出错: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    def analyze_file_content(self, file_path: str) -> Dict:
        """分析文件内容"""
        try:
            # 检查文件类型
            file_extension = file_path.split('.')[-1].lower()
            
            # 读取文件内容
            success = False
            content = ""
            columns = []
            
            if file_extension in self.document_extensions:
                if file_extension in ['xlsx', 'xls']:
                    success, content, columns = self.read_excel_content(file_path)
                elif file_extension == 'csv':
                    success, content, columns = self.read_csv_content(file_path)
            elif file_extension in self.image_extensions:
                result = self.analyze_image_content(file_path)
                return result
            
            if not success:
                return {
                    "success": False,
                    "error": "无法读取文件内容"
                }
            
            return {
                "success": True,
                "content": content,
                "columns": columns,
                "file_type": file_extension
            }
            
        except Exception as e:
            logger.error(f"分析文件内容出错: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    async def analyze_file(self, url: str) -> Dict:
        """分析文件"""
        try:
            # 下载文件
            file_path = await self.download_file(url)
            if not file_path:
                return {
                    "success": False,
                    "error": "文件下载失败"
                }
            
            # 检查是否是压缩文件
            file_extension = file_path.split('.')[-1].lower()
            if file_extension in self.archive_extensions:
                # 解压文件
                extracted_files = self.extract_archive(file_path)
                if not extracted_files:
                    return {
                        "success": False,
                        "error": "解压文件失败"
                    }
                
                # 分析解压后的文件
                results = []
                for extracted_file in extracted_files:
                    ext = extracted_file.split('.')[-1].lower()
                    if ext in self.document_extensions + self.image_extensions:
                        result = self.analyze_file_content(extracted_file)
                        if result["success"]:
                            results.append(result)
                
                # 清理临时文件
                try:
                    os.remove(file_path)
                    for extracted_file in extracted_files:
                        os.remove(extracted_file)
                except Exception as e:
                    logger.warning(f"清理临时文件失败: {str(e)}")
                
                return {
                    "success": True,
                    "results": results
                }
            else:
                # 直接分析文件
                result = self.analyze_file_content(file_path)
                
                # 清理临时文件
                try:
                    os.remove(file_path)
                except Exception as e:
                    logger.warning(f"清理临时文件失败: {str(e)}")
                
                return {
                    "success": True,
                    "results": [result] if result["success"] else []
                }
            
        except Exception as e:
            logger.error(f"分析文件出错: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            } 