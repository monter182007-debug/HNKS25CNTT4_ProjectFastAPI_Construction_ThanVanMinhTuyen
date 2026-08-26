from fastapi import HTTPException,status
from core.security import hash_password,verify_password,SECRET_KEY, ALGORITHM,generate_user_token
from sqlalchemy.orm import Session
from models.user import UserModel
from schemas.user import UserCreate
from typing import Optional
import jwt

# Hàm đăng ký tài khoản
def create_user_service(user_data:UserCreate,db:Session,role_name: str = "USER"):
    # Check email trùng lặp
    existing_user = db.query(UserModel).filter(UserModel.email == user_data.email).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email này đã được đăng ký, vui lòng sử dụng email khác."
        )

    hashed_pwd = hash_password(user_data.password)

    new_user = UserModel(
        email=user_data.email,
        password_hash=hashed_pwd,
        full_name=user_data.full_name, 
        role=role_name
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# Hàm đăng nhập tài khoản
def authenticate_user(db:Session,email:str,password:str):
    user = db.query(UserModel).filter(UserModel.email == email).first()

    if not user:
        return None

    if not verify_password(password,user.password_hash):
        return None

    return user

# Hàm để kiểm tra loại refresh và trả ra toke mới 
def refresh_token_service(refresh_token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Refresh token không hợp lệ hoặc đã hết hạn"
    )
    try:
        # Giải mã token
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Kiểm tra xem có đúng là loại "refresh" token hay không
        if payload.get("type") != "refresh":
            raise credentials_exception
            
        user_id = payload.get("user_id")
        email = payload.get("sub")
        role = payload.get("role")
        
        # Cấp lại một Access Token mới tinh
        new_access_token = generate_user_token(
            user_id=user_id,
            email=email,
            role=role
        )
        
        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }
    except Exception:
        raise credentials_exception


