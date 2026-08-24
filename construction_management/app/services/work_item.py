from sqlalchemy.orm import Session
from typing import Optional
from fastapi import HTTPException,status
from models.user import UserModel
from models.work_item import WorkItemModel
from models.site import ConstructionSiteModel,SiteMemberModel
from schemas.work_item import WorkItemCreate,WorkItemUpdate
from datetime import datetime

# Hàm thêm mới danh mục thi công
def create_work_item_service(db:Session,site_id:int,item_data:WorkItemCreate,current_user:dict):
    # Kiểm tra xemc công trình có tồn tại ko 
    site = db.query(ConstructionSiteModel).filter(
        ConstructionSiteModel.id == site_id,
        ConstructionSiteModel.is_deleted == False
    ).first()

    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy công trình này"
        )

    # Kiểm tra xem có phải thành viên của công trình ko
    is_member = db.query(SiteMemberModel).filter(
        SiteMemberModel.site_id == site_id,
        SiteMemberModel.user_id == current_user["user_id"]
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền tạo hạng mục thi công cho công trình này."
        )

    # Kiểm tra xem ASSIGNEE nếu gán phụ trách phải thuộc công trình 
    if item_data.assignee_id:
        assignee_check= db.query(SiteMemberModel).filter(
            SiteMemberModel.site_id == site_id,
            SiteMemberModel.user_id == item_data.assignee_id
        ).first()

        if not assignee_check:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Thành viên được phân công không thuộc công trình này."
            )   

    new_work_item = WorkItemModel(
        site_id=site_id,
        title=item_data.title.strip(),
        description=item_data.description,
        assignee_id=item_data.assignee_id,
        status=item_data.status if item_data.status else "TODO",
        priority=item_data.priority if item_data.priority else "MEDIUM",
        due_date=item_data.due_date,
        created_at=datetime.now()
    )

    db.add(new_work_item)
    db.commit()
    db.refresh(new_work_item)

    return new_work_item

# Hàm xem danh sách hạng mục thi công
def get_work_items_service(
    db: Session, 
    site_id: int, 
    current_user: dict,
    statuss: Optional[str] = None,
    priority: Optional[str] = None,
    assignee_id: Optional[int] = None,
    search: Optional[str] = None,
    skip:int = 0, # bỏ qua bao nhiêu bản ghi
    limit : int = 1, # Lấy tối đa bao nhiêu bản ghi
    sort_by :str = "created_at",
    order :str = "desc"
    ):
    # 1. Kiểm tra công trình có tồn tại và chưa bị xóa mềm không
    site = db.query(ConstructionSiteModel).filter(
        ConstructionSiteModel.id == site_id,
        ConstructionSiteModel.is_deleted == False
    ).first()

    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy công trình này."
        )

    # 2. Kiểm tra user hiện tại có thuộc công trình này không
    is_member = db.query(SiteMemberModel).filter(
        SiteMemberModel.site_id == site_id,
        SiteMemberModel.user_id == current_user["user_id"]
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền xem hạng mục thi công của công trình này."
        )

    # 3. Lấy đúng các hạng mục thi công thuộc site_id này
    query = db.query(WorkItemModel).filter(
        WorkItemModel.site_id == site_id
        # ,WorkItemModel.is_deleted == False
        )
    # Áp dụng các điều kiện search và filter
    if statuss:
        query = query.filter(WorkItemModel.status == str(statuss))
    if priority:
        query = query.filter(WorkItemModel.priority == priority)

    if assignee_id:
        query = query.filter(WorkItemModel.assignee_id == assignee_id)

    if search:
        query = query.filter(WorkItemModel.title.ilike(f"%{search}%"))

    # Áp dụng Sắp xếp (Sorting)
    # getattr(đối_tượng, "tên_thuộc_tính_dạng_chuỗi", giá_trị_mặc_định) để xem người dùng có truyền đúng 1 cột trong bảng đó 
    sort_column = getattr(WorkItemModel,sort_by,WorkItemModel.created_at)
    if order.lower() == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    # Phân trang
    work_items = query.offset(skip).limit(limit).all()
    return work_items



# Hàm xem danh sách hạng mục thi công
def get_work_item_detail_service(db:Session,work_item_id:int,current_user:dict):
    # Tìm hạng mục thi công theo id
    work_item = db.query(WorkItemModel).filter(
        WorkItemModel.id == work_item_id
        # WorkItemModel.is_deleted == False
        ).first()

    if not work_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy hạng mục thi công này."
        )

    # Kiểm tra xem user hiện tai có thuộc công trình chứa hạng mục này ko

    is_member = db.query(SiteMemberModel).filter(
        SiteMemberModel.site_id == work_item.site_id,
        SiteMemberModel.user_id == current_user["user_id"]
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền xem hạng mục thi công này vì không thuộc công trình tương ứng."
        )

    return work_item


# Hàm cập nhật các hạng mục thi công
def update_update_work_item_service(db:Session,work_item_id:int,item_data:WorkItemUpdate,current_user:dict):
    # Tìm hạng mục theo ID
    work_item = db.query(WorkItemModel).filter(WorkItemModel.id == work_item_id).first()

    if not work_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy hạng mục thi công này."
        )

    # Kiểm tra xem user có thuộc công trình chứa hạng mục này ko
    is_member = db.query(SiteMemberModel).filter(
        SiteMemberModel.site_id == work_item.site_id,
        SiteMemberModel.user_id == current_user["user_id"]
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền cập nhật hạng mục thi công này."
        )
    # Kiểm tra quyền hạn
    is_owner = (is_member.role == "OWNER") 
    is_assignee = (work_item.assignee_id == current_user["user_id"])

    if not (is_owner or is_assignee):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền chỉnh sửa hạng mục này (Chỉ Owner hoặc người được Assign mới được phép)."
        )
    
    # Lấy dữ liệu cần cập nhật
    update_data = item_data.model_dump(exclude_unset=True)

    # 4. Nếu có cập nhật assignee_id, phải kiểm tra user đó có thuộc công trình không
    if "assignee_id" in update_data and update_data["assignee_id"] is not None:
        assignee_check = db.query(SiteMemberModel).filter(
            SiteMemberModel.site_id == work_item.site_id,
            SiteMemberModel.user_id == update_data["assignee_id"]
        ).first()

        if not assignee_check:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Không thể phân công cho người dùng không thuộc công trình này."
            )

    # Cập nhật 
    for key,value in update_data.items():
        setattr(work_item,key,value)

    db.commit()
    db.refresh(work_item)
    return work_item

# Hàm xóa hạng mục thi công
def delete_work_item_service(db:Session,work_item_id:int,current_user:dict):
    # Tìm hạng mục thi công 
    work_item = db.query(WorkItemModel).filter(
        WorkItemModel.id == work_item_id
      # WorkItemModel.is_deleted == False
    ).first()

    if not work_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy hạng mục thi công này."
        )

    # Kiểm tra user 
    is_member = db.query(SiteMemberModel).filter(
        SiteMemberModel.site_id == work_item.site_id,
        SiteMemberModel.user_id == current_user["user_id"]
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không thuộc công trình này."
        )

    if is_member.role != "OWNER":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền xóa hạng mục thi công này (Chỉ Owner mới được xóa)."
        )
    # Xóa cứng 
    db.delete(work_item)

    # Xóa mềm 
    # work_item.is_deleted = True
    # work_item.deleted_at = datetime.now()
    db.commit()
    return {"message": "Đã xóa hạng mục thi công thành công."}