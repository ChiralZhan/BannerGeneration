from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, String, DateTime
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Enum, ForeignKey
import base64

from utils.config import Config

# 数据库配置
engine = create_engine(Config.DATABASE_URL, echo=True)
Base = declarative_base()
Base.metadata.bind = engine

# 创建数据库引擎
Session = sessionmaker(bind=engine)

# 定义User模型

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    last_login_time = Column(DateTime)
    role = Column(String, nullable=False)

    def verify_password(self, input_password):
        return check_password_hash(self.password, input_password)


def authenticate(username, password):
    """ 验证用户登录，并在成功时更新最后登录时间。"""
    session = Session()
    try:
        user = session.query(User).filter(User.username == username).one_or_none()
        if user and user.verify_password(password):
            user.last_login_time = datetime.utcnow()
            session.commit()
            return True
        return False
    except Exception as e:
        print(f"Authentication error: {e}")
        session.rollback()
        return False
    finally:
        session.close()


def create_user(username, password):
    """ 创建新用户，存储加密的密码。"""
    encrypted_password = generate_password_hash(password)
    new_user = User(username=username, password=encrypted_password)
    session = Session()
    try:
        session.add(new_user)
        session.commit()
    except Exception as e:
        print(f"Error creating user: {e}")
        session.rollback()
    finally:
        session.close()


def encrypt_data(data):
    return base64.b64encode(data.encode()).decode('utf-8')


def decrypt_data(data):
    return base64.b64decode(data.encode()).decode('utf-8')


def fetch_user_id(username):
    session = Session()
    user = session.query(User).filter_by(username=username).one_or_none()
    session.close()
    if user:
        return user.id
    return None


def fetch_user_by_username(username):
    session = Session()
    user = session.query(User).filter(User.username == username).one_or_none()
    session.close()
    return user


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
    creation_time = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum('pending', 'completed', 'failed', name='task_statuses'))
