from fastapi import APIRouter,Depends,status,HTTPException
from db.database import get_db
from schemas.user import UserCreate,UserResponse,UserLogin
from sqlalchemy.orm import Session
from services.auth import create_user_service,authenticate_user
from core.security import generate_user_token


router = APIRouter(prefix="/auth",tags=["Authentication"])

# Phần đăng ký
@router.post("/register",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def register_user(user_data:UserCreate,db:Session = Depends(get_db)):
    return create_user_service(user_data,db)

# Phần đăng nhập
@router.post("/login")
def login_user(login_data:UserLogin,db:Session = Depends(get_db)):
    user = authenticate_user(db,email=login_data.email,password=login_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tài khoản hoặc mật khẩu không chính xác"
        )

    # Xem tài khoản bị khóa ko
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tài khoản của bạn đã bị vô hiệu hóa"
        )

    access_token = generate_user_token(
        user_id=user.id,
        email=user.email,
        role=user.role
    )
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }