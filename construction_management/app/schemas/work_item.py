from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

# Class Base chứa thông tin chung
class WorkItemBase(BaseModel):
    title:str
    description:Optional[str] = None
    status:Optional[str] = "TODO"
    priority:Optional[str] = "MEDIUM"
    due_date: Optional[datetime] = None

# Class Base chứa thêm mới 
class WorkItemCreate(WorkItemBase):
    assignee_id:Optional[int] = None
# Class Base cập nhật
class WorkItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    assignee_id: Optional[int] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None

# Class trả về dữ liệu Client
class WorkItemResponse(WorkItemBase):
    id: int
    site_id: int
    assignee_id: Optional[int] = None
    created_at: datetime
    # Giúp pydantic đọc dữ liệu từ SQL  
    model_config = ConfigDict(from_attributes=True)