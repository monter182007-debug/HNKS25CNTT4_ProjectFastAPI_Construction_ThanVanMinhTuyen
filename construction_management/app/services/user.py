from sqlalchemy.orm import Session
from models.user import UserModel
from typing import Optional

# Hàm chỉ lấy ra profile cá nhân
def get_user_by_id(db:Session,user_id:int):
    return db.query(UserModel).filter(UserModel.id==user_id).first()


# Hàm tìm kiếm lọc trả về toàn bộ User cho ADMIN
def get_all_users_service(db:Session,search:Optional[str]=None,is_active:Optional[bool]=None):

    query = db.query(UserModel)
    # Nếu người dùng nhập lọc theo tên và email
    if search:
        query = query.filter((UserModel.full_name.contains(search)) | (UserModel.email.contains(search)))

    # Nếu lọc theo trạng thái
    if is_active is not None:
        query = query.filter(UserModel.is_active == is_active)

    return query.all()