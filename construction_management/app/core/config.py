import os
from dotenv import load_dotenv

# Tai cac file .env vao bien moi trường
load_dotenv()

# Thiet lap cau hinh trung tam 
class Settings:
    DATABASE_URL: str | None = os.getenv("DATABASE_URL")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    SECRET_KEY: str | None = os.getenv("SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 30))

settings = Settings()

