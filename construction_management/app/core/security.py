import bcrypt
import jwt
import time
from core.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.JWT_ALGORITHM

# Hàm băm mật khẩu
def hash_password(password:str) -> str:
    # Chuyển mật khẩu thành dạng bytes
    password_bytes = password.encode()

    # Tạo muối salt ngẫu nhiên
    salt = bcrypt.gensalt()

    # Băm mật khẩu
    hashed_bytes = bcrypt.hashpw(password_bytes,salt)
    # Đưa về dạng string
    return hashed_bytes.decode()


# Hàm đối chiếu mật khẩu
def verify_password(plain_password:str,hashed_password:str) -> bool:
    return bcrypt.checkpw(plain_password.encode(),hashed_password.encode())

# Hàm tạo JWT Access Token cấp cho Client
def generate_user_token(user_id: int, email:str,role:str) -> str:
    payload={
        "sub": email,
        "user_id": user_id,
        "role": role,
        "exp": int(time.time()) + 1800
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)