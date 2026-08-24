from fastapi import HTTPException,status
from core.security import hash_password,verify_password
from sqlalchemy.orm import Session
from models.user import UserModel
from schemas.user import UserCreate
from typing import Optional

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


