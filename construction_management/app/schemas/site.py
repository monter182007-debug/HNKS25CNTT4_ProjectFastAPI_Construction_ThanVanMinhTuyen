from pydantic import BaseModel, ConfigDict,Field
from typing import Optional
from datetime import datetime

# Class Base chứa thông tin chung
class ConstructionSiteBase(BaseModel):
    name: str
    description: Optional[str] = None

# Class Base chứa thêm mới 
class ConstructionSiteCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Tên công trình không được để trống")
    description: Optional[str] = None

# Class Base cập nhật
class ConstructionSiteUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

# Class trả về dữ liệu Client
class ConstructionSiteResponse(ConstructionSiteBase):
    id: int
    owner_id: int
    created_at: datetime

    # Giúp pydantic đọc dữ liệu từ SQL
    model_config = ConfigDict(from_attributes=True)


# Schemas Thành viên 
# Class Base chứa thông tin chung
class SiteMemberBase(BaseModel):
    role:str

# Class Base chứa thêm mới 
class SiteMemberCreate(BaseModel):
    user_id: int
    # role: Optional[str] = "MEMBER"

# Class trả về dữ liệu Client
class SiteMemberResponse(SiteMemberBase):
    site_id: int
    user_id: int
    joined_at: datetime

    # Giúp pydantic đọc dữ liệu từ SQL
    model_config = ConfigDict(from_attributes=True)