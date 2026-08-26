from sqlalchemy.orm import Session
from schemas.comment import CommentCreate
from models.work_item import WorkItemModel
from fastapi import HTTPException,status
from models.site import SiteMemberModel
from models.comment import CommentModel
from datetime import datetime

# Hàm tạo comment ghi chú cho hạng mục thi công
def create_comment_service(db:Session,work_item_id:int,comment_data:CommentCreate,current_user:dict):
    # 1. Kiểm tra hạng mục thi công có tồn tại ko
    work_item = db.query(WorkItemModel).filter(WorkItemModel.id == work_item_id).first()

    if not work_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy hạng mục thi công này."
        )

    # 2. Kiểm tra xem có phải thành viên của công trình trong hạng mục ko
    is_member = db.query(SiteMemberModel).filter(
        SiteMemberModel.site_id == work_item.site_id,
        SiteMemberModel.user_id == current_user["user_id"]
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không phải thành viên công trình nên không thể viết comment."
        )

    # Tạo mới comment 
    new_comment = CommentModel(
        work_item_id = work_item_id,
        user_id = current_user["user_id"],
        content=comment_data.content.strip(),
        created_at = datetime.now()
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment

# Hàm xem ghi chú hạng mục thi công
def get_comments_service(db:Session,work_item_id:int,current_user:dict):
    # Kiểm tra hạng mục tồn tại ko
    work_item = db.query(WorkItemModel).filter(WorkItemModel.id == work_item_id).first()

    # Kiểm tra quyền thành viên công trình
    is_member = db.query(SiteMemberModel).filter(
        SiteMemberModel.site_id == work_item.site_id,
        SiteMemberModel.user_id == current_user["user_id"]
    ).first()

    if not is_member:
        raise HTTPException(status_code=403, detail="Bạn không có quyền xem nhật ký comment của công trình này.")

    comments = db.query(CommentModel).filter(CommentModel.work_item_id == work_item_id).all()

    return comments




