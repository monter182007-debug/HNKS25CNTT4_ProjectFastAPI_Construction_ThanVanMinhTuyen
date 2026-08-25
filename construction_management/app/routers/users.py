from fastapi import APIRouter,Depends,status,HTTPException
from schemas.user import UserResponse
from dependencies.auth import get_current_user
from db.database import get_db
from sqlalchemy.orm import Session
from models.user import UserModel
from services.user import get_all_users_service,get_user_by_id
from typing import Optional
from dependencies.role_checker import require_admin

router = APIRouter(prefix="/users", tags=["Users"])

# Giúp xem profile cá nhân
@router.get("/me", response_model=UserResponse)
def get_my_profile(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user.get("user_id")
    user = get_user_by_id(db, user_id=user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy người dùng"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tài khoản này đã bị khóa, không có quyền truy cập."
        )
    return user


@router.get("/", response_model=list[UserResponse])
def get_all_users(
    search: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    admin_user: dict = Depends(require_admin)
):
    return get_all_users_service(db, search=search, is_active=is_active)