from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite数据库URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./todo.db"

# 创建SQLAlchemy引擎
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 创建数据库会话类
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类
Base = declarative_base()

def init_db():
    # 导入所有模型以确保它们在创建数据库表之前被注册
    from models import Todo
    Base.metadata.create_all(bind=engine)