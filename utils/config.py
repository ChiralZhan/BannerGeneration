import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # 数据库配置
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost/mydatabase')
    FONT_PATH = '方正兰亭中黑简体.TTF'
    SDWEBUI_URL ='127.0.0.1:8080' #add your stable diffusion webui url here
