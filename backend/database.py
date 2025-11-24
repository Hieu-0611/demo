import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Lấy URL từ biến môi trường (Environment Variable)
# - Trên Render: Nó sẽ lấy link Aiven từ biến "DATABASE_URL" mà bạn cấu hình.
# - Trên máy bạn: Nó không tìm thấy biến đó, nên sẽ dùng cái link localhost phía sau.
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+mysqlconnector://root:@localhost/loveconnect")

# 2. Fix lỗi tương thích driver trên Cloud
# Link Aiven thường bắt đầu bằng 'mysql://', nhưng SQLAlchemy trên Linux thích 'mysql+pymysql://' hơn
if DATABASE_URL.startswith("mysql://"):
    DATABASE_URL = DATABASE_URL.replace("mysql://", "mysql+pymysql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()