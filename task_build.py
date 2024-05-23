from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from utils.config import Config
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    last_login_time = Column(DateTime)
    role = Column(String, nullable=False)

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    task_type = Column(Enum('local_upload', 'material_library', 'ai_drawing', name='task_types'))
    input_parameters = Column(Text)  # JSON format
    output_image_path = Column(String)
    image_format = Column(String)
    service_info = Column(String)
    drawing_time = Column(DateTime)
    creation_time = Column(DateTime, default=datetime.UTC)
    status = Column(Enum('pending', 'completed', 'failed', name='task_statuses'))

# 数据库配置
DATABASE_URL = Config.DATABASE_URL
engine = create_engine(DATABASE_URL, echo=True)  # echo=True for debugging

# 创建表
Base.metadata.create_all(engine)