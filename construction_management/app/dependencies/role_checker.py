from fastapi import Depends,HTTPException,status
from dependencies.auth import get_current_user

# Hàm kiểm tra quyền Admin
def require_admin(current_user:dict = Depends(get_current_user)):
    # Kiểm tra xem tài khoản có p Admin
    user_role = current_user.get("role", "")
    if user_role.upper() != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền truy cập tính năng này (Yêu cầu quyền ADMIN)"
        )

    return current_user