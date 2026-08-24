from sqlalchemy.orm import Session
from models.activity_log import ActivityLogModel
from typing import Optional
from datetime import datetime
# Hàm lưu lại lịch sử hoạt động người dùng
def log_activity(db:Session,user_id: int, action: str, site_id: int = None, description: Optional[str] = None):
    new_log = ActivityLogModel(
        user_id=user_id,
        site_id=site_id,
        action=action,
        description=description,
        created_at=datetime.now().isoformat()
    )
    db.add(new_log)
    db.commit()