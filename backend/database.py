import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Lấy URL từ biến môi trường
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+mysqlconnector://root:@localhost/loveconnect")

# 2. Fix lỗi tương thích driver trên Cloud (Render)
if DATABASE_URL.startswith("mysql://"):
    DATABASE_URL = DATABASE_URL.replace("mysql://", "mysql+pymysql://", 1)

# 3. 🚨 QUAN TRỌNG: Loại bỏ tham số '?ssl-mode=REQUIRED' gây lỗi
if "?ssl-mode=" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.split("?")[0]  # Cắt bỏ phần query string

# 4. Tạo Engine với cấu hình SSL (nếu cần thiết)
# Trên Render/Aiven, thường chỉ cần URL sạch là tự chạy được SSL
connect_args = {}
if "aivencloud.com" in DATABASE_URL:
    connect_args = {"ssl": {"ssl_mode": "REQUIRED"}} # Hoặc "PREFERRED"

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True, # Giúp tự động kết nối lại nếu bị ngắt
    pool_recycle=3600
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()