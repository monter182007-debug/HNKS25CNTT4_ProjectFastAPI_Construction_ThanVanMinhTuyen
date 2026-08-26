from db.database import Base
from sqlalchemy import Column,Integer,String,Boolean,DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    email = Column(String(100),unique=True,nullable=False)
    password_hash = Column(String(255),nullable=False)
    full_name = Column(String(100),nullable=False)
    role = Column(String(50),default="USER")
    is_active = Column(Boolean,default=True)
    created_at = Column(DateTime,nullable=False,default=func.now())

    # 1 User làm chủ N Công trình
    owned_sites = relationship("ConstructionSiteModel", back_populates="owner")

    # 1 User - N Hạng mục thi công
    assigned_work_items = relationship("WorkItemModel", back_populates="assignee")

    # 1 User tham gia nhiều công trình (Bảng trung gian)
    joined_sites = relationship("SiteMemberModel", back_populates="user")


