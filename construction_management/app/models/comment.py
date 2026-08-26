from sqlalchemy import Column,Integer,String,DateTime,Text,ForeignKey
from db.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime

# Models để Comment (Ghi chú nhật ký thi công cho hạng mục)
class CommentModel(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    work_item_id = Column(Integer, ForeignKey("work_items.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    # MQH 
    work_item = relationship("WorkItemModel",backref="comments") #backref: giúp tạo 1 thuộc tính ảo bên bảng work_items
    user = relationship("UserModel")
