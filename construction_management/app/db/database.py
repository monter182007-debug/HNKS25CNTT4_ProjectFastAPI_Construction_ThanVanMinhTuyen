from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from core.config import settings

# Khởi tạo lưu đường dẫn
engine = create_engine(settings.DATABASE_URL)

# Tạo phiên làm việc
SessionLocal = sessionmaker(
    autoflush=False,
    autocommit = False,
    bind=engine,
    expire_on_commit=False
)

# Lớp để tạo bảng models
Base = declarative_base()

# Hàm để cung cấp kết nối cho API
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

        