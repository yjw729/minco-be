from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from urllib.parse import quote_plus as urlquote
from contextlib import contextmanager

DB_URL = "mindco_user:Mindco777#@182.92.216.167/mindco_db" 
MAX_POOL_SIZE = 5

engine = create_engine(
    f"mysql+pymysql://{DB_URL}",
    max_overflow=MAX_POOL_SIZE,
    pool_timeout=10,
    pool_recycle=3600,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

@contextmanager
def get_db_session():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """创建所有表"""
    Base.metadata.create_all(bind=engine)

def drop_tables():
    """删除所有表"""
    Base.metadata.drop_all(bind=engine)

class UserModel(Base):
    """用户表"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255))
    password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    avatar = Column(String(500))
    personal_tags = Column(JSON)
    long_term_goals = Column(JSON)
    recent_focus = Column(JSON)
    daily_plan_time = Column(String(10))
    daily_review_time = Column(String(10))
    timezone = Column(String(50))
    status = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), server_onupdate=text("CURRENT_TIMESTAMP"))

class TaskModel(Base):
    """任务表"""
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    title = Column(String(255))
    description = Column(Text)
    status = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), server_onupdate=text("CURRENT_TIMESTAMP"))

if __name__ == "__main__":
    create_tables()
    # drop_tables() 