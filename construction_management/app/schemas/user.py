from pydantic import BaseModel,EmailStr,ConfigDict,Field
from typing import Optional
from datetime import datetime

# Class Base của User
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: Optional[str] = "USER"
    is_active: Optional[bool] = True

# Class Base tạo mới
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    full_name: str = Field(min_length=2)

# Class Base cập nhật
class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

# Class Base đinh dạng trả về người dùng
class UserResponse(UserBase):
    id: int
    created_at: datetime
    # Giúp pydantic đọc dữ liệu từ SQL
    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


# Schemas nhận refersh 
class RefreshTokenRequest(BaseModel):
    refresh_token: str