from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer,APIKeyHeader,HTTPBearer,HTTPAuthorizationCredentials
import jwt
import jwt.exceptions

from core.config import settings

# Tạo ra bảo vệ trước khi vào phải đăng nhâp
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
security= HTTPBearer()

def get_current_user(credentials:HTTPAuthorizationCredentials=Depends(security)) -> dict:
    # Lấy token thô bỏ chữ Bearer
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Thẻ từ không hợp lệ hoặc ko thể xác thực"
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        email:str = payload.get("sub")
        user_id :int = payload.get("user_id")

        # Kiểm tra refresh token
        token_type = payload.get("type")
        if token_type == "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Không thể dùng Refresh Token để truy cập tài nguyên này"
            )

        if email is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Thẻ từ hợp lệ nhưng bị thiếu thông tin định danh (Email hoặc ID)"
            )

        return payload
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Thẻ từ đã hết hạn, vui lòng đăng nhập lại",
        )
    except jwt.exceptions.PyJWTError:
        raise credentials_exception