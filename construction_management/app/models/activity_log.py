from sqlalchemy import Column,Integer,String,ForeignKey,Text
from db.database import Base


# Mode để lưu lại lịch sử hoạt đông
class ActivityLogModel(Base):
    __tablename__ = "activity_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    site_id = Column(Integer, ForeignKey("construction_sites.id", ondelete="CASCADE"), nullable=True)
    action = Column(String(100), nullable=False) 
    description = Column(Text, nullable=True)    
    created_at = Column(String(50))