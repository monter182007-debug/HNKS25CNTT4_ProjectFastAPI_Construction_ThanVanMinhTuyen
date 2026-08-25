from db.database import Base
from sqlalchemy import Column,Integer,String,Text,ForeignKey,DateTime,Enum,Boolean
from sqlalchemy.orm import relationship

class WorkItemModel(Base):
    __tablename__ = "work_items"
    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer,ForeignKey("construction_sites.id"),nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text,nullable=False)
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(Enum("TODO", "IN_PROGRESS", "DONE", name="work_status_enum"), nullable=False, default="TODO")
    priority = Column(Enum("LOW", "MEDIUM", "HIGH", name="work_priority_enum"), nullable=False, default="MEDIUM")
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime,nullable=False)

    # Thực hiện xóa mềm
    # is_deleted = Column(Boolean, default=False)
    # deleted_at = Column(DateTime, nullable=True)

    # N Hạng mục - 1 Công trình
    site = relationship("ConstructionSiteModel", back_populates="work_items")

    # N Hạng mục - 1 User 
    assignee = relationship("UserModel", back_populates="assigned_work_items")
