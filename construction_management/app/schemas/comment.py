from pydantic import BaseModel,ConfigDict,Field
from datetime import datetime

# Schemas để thêm mới comment
class CommentCreate(BaseModel):
    content:str = Field(min_length=1, description="Nội dung nhật ký thi công không được để trống")

# Schemas để trả về response 
class CommentResponse(BaseModel):
    id:int
    work_item_id:int
    user_id:int
    content:str
    created_at:datetime
    # Giúp pydantic đọc dữ liệu từ SQL
    model_config = ConfigDict(from_attributes=True)