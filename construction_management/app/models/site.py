from db.database import Base
from sqlalchemy import Column,Integer,String,Text,ForeignKey,DateTime,Boolean
from sqlalchemy.orm import relationship


# Class cho construction
class ConstructionSiteModel(Base):
    __tablename__="construction_sites"
    id = Column(Integer, primary_key=True, index=True)
    name= Column(String(255),nullable=False)
    description =Column(Text)
    owner_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    created_at = Column(DateTime,nullable=False)

    # Cột theo dõi xóa mềm
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(String(50), nullable=True)
        
    # N công trình do 1 User 
    owner = relationship("UserModel", back_populates="owned_sites")

    # 1 Công trình - N Hạng mục thi công
    work_items = relationship("WorkItemModel", back_populates="site")

    # 1 Công trình - N thành viên (Bảng trung gian)
    members = relationship("SiteMemberModel", back_populates="site",cascade="all, delete-orphan")

# Class cho sitmembers
class SiteMemberModel(Base):
    __tablename__ ="site_members"
    site_id = Column(Integer,ForeignKey("construction_sites.id",ondelete="CASCADE"),primary_key=True)
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    role = Column(String(50), nullable=False)
    joined_at = Column(DateTime,nullable=False)

    # Liên kết tới User 
    user = relationship("UserModel", back_populates="joined_sites")

    # Liên kết tới công trình
    site = relationship("ConstructionSiteModel", back_populates="members")