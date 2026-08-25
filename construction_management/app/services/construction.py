from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from models.site import ConstructionSiteModel,SiteMemberModel
from models.user import UserModel
from schemas.site import ConstructionSiteCreate,SiteMemberCreate
from datetime import datetime
from typing import Optional
from utils.logger_helper import log_activity

# Hàm tạo công trình
def create_construction_site_service(db:Session,site_data:ConstructionSiteCreate,current_user:dict):
    # Kiểm tra công trình bị trùng tên ko
    existing_site = db.query(ConstructionSiteModel).filter(ConstructionSiteModel.name.ilike(f"%{site_data.name.strip()}%")).first()

    if existing_site:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tên công trình này đã tồn tại trong hệ thống."
        )

    new_site = ConstructionSiteModel(
        name=site_data.name.strip(),
        description=site_data.description,
        owner_id=current_user["user_id"],
        created_at=datetime.now().isoformat()
    )

    db.add(new_site)
    db.commit()
    # Lưu lại lịch sử
    log_activity(db, user_id=current_user["user_id"], action="CREATE_SITE", site_id=new_site.id, description=f"Đã tạo công trình: {new_site.name}")
    db.refresh(new_site)

    # Thêm người tạo thành OWNER
    new_member = SiteMemberModel(
        site_id=new_site.id,
        user_id=current_user["user_id"],
        role="OWNER",
        joined_at=datetime.now().isoformat()
    )

    db.add(new_member)
    db.commit()
    db.refresh(new_member)

    return new_site

# Hàm lấy danh sách công trình
def get_user_construction_sites_service(db:Session,current_user:dict,search:Optional[str]=None):
    # Join vào bảng sitemember để kiểm tra 
    query = db.query(ConstructionSiteModel).join(
        SiteMemberModel, ConstructionSiteModel.id == SiteMemberModel.site_id
    ).filter(
        SiteMemberModel.user_id == current_user["user_id"],
        ConstructionSiteModel.is_deleted == False
    )
    
    # Nếu có từ khóa tìm kiếm thì lọc theo tên
    if search:
        query = query.filter(ConstructionSiteModel.name.ilike(f"%{search}%"))
        
    return query.all()

# Xem chi tiết công trình
def get_construction_site_detail_service(db:Session,site_id:int,current_user:dict):
    # Kiểm tra công trình có trong DB 
    site = db.query(ConstructionSiteModel).filter(ConstructionSiteModel.id == site_id,ConstructionSiteModel.is_deleted == False).first()

    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy công trình này."
        )

    # Kiểm tra user hiện tại có thuộc công trình này ko
    is_member = db.query(SiteMemberModel).filter(
        SiteMemberModel.site_id == site_id,
        SiteMemberModel.user_id == current_user["user_id"]
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền truy cập vào công trình này."
        )

    return site

# Hàm cập nhật Công trình
def update_construction_site_service(db:Session,site_id:int,site_data:ConstructionSiteCreate,current_user:dict):

    # Kiểm tra quyền OWNER 
    member = db.query(SiteMemberModel).filter(
        SiteMemberModel.site_id == site_id,
        SiteMemberModel.user_id == current_user["user_id"],
        SiteMemberModel.role == "OWNER"
    ).first()

    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ OWNER mới được sửa công trình"
        )

    # Kiểm tra công trình

    site = db.query(ConstructionSiteModel).filter(ConstructionSiteModel.id == site_id).first()

    if not site:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy công trình")

    # Cập nhật tự động dùng vòng lặp
    site_data_dict = site_data.dict(exclude_unset=True) # Chỉ lấy những trường người dùng nhập lên

    for key,value in site_data_dict.items():
        setattr(site,key,value)

    db.commit()

    # Hàm lưu lịch sử
    log_activity(db, user_id=current_user["user_id"], action="UPDATE_SITE", site_id=site.id, description=f"Đã cập nhật công trình ID: {site.id}")

    db.refresh(site)
    return site

# Hàm xóa công trình 
def delete_construction_site_service(db:Session,site_id:int,current_user:dict):
    # Kiểm tra quyền OWNER
    member = db.query(SiteMemberModel).filter(
        SiteMemberModel.site_id == site_id,
        SiteMemberModel.user_id == current_user["user_id"],
        SiteMemberModel.role == "OWNER"
    )

    if not member:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Chỉ OWNER mới được xóa công trình")

    site = db.query(ConstructionSiteModel).filter(
        ConstructionSiteModel.id == site_id,
        ConstructionSiteModel.is_deleted == False
        ).first()
    if not site:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy công trình")

    # Thực hiện xóa mềm
    site.is_deleted = True
    site.deleted_at = datetime.now().isoformat()

    db.commit()
    return {"detail": "Đã chuyển công trình vào thùng rác (Xóa mềm thành công)"}


# Hàm thêm thành viên vào công trình
def add_site_member_service(db:Session,site_id:int,member_data:SiteMemberCreate,current_user:dict):
    # Kiểm tra xem có phải OWNER 
    member = db.query(SiteMemberModel).filter(
        SiteMemberModel.site_id == site_id,
        SiteMemberModel.user_id == current_user["user_id"],
        SiteMemberModel.role == "OWNER"
    ).first()

    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ OWNER mới có quyền thêm thành viên vào công trình."
        )

    # Kiểm tra xem user cần thêm có tồn tại
    target_user = db.query(UserModel).filter(UserModel.id == member_data.user_id).first()

    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy người dùng cần thêm trong hệ thống."
        )

    # Kiểm tra xem đã là thành viên công trình chưa
    existing_member = db.query(SiteMemberModel).filter(
        SiteMemberModel.site_id == site_id,
        SiteMemberModel.user_id == member_data.user_id
    ).first()

    if existing_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Người dùng này đã là thành viên của công trình rồi."
        )

    # Thêm mới
    new_member = SiteMemberModel(
        site_id=site_id,
        user_id=member_data.user_id,
        role="MEMBER",
        joined_at=datetime.now().isoformat()
    )

    db.add(new_member)
    db.commit()

    # Hàm lưu lịch sử
    log_activity(db, user_id=current_user["user_id"], action="ADD_MEMBER", site_id=site_id, description=f"Đã thêm user_id {member_data.user_id} vào công trình")

    db.refresh(new_member)

    return new_member

# Hàm xóa thành viên trong công trình
def remove_site_member_service(db:Session,site_id:int,target_user_id:int,current_user:dict):
    # Kiểm tra xem có phải OWNER 
    current_owner_check = db.query(SiteMemberModel).filter(
        SiteMemberModel.site_id == site_id,
        SiteMemberModel.user_id == current_user["user_id"],
        SiteMemberModel.role == "OWNER"
    ).first()

    if not current_owner_check:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ OWNER mới có quyền xóa thành viên khỏi công trình."
        )

    # Tìm thành viên cần xóa trong công trình
    target_member = db.query(SiteMemberModel).filter(
        SiteMemberModel.site_id == site_id,
        SiteMemberModel.user_id == target_user_id
    ).first()


    if not target_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy thành viên này trong công trình."
        )
    owner_count = 0
    # Kiểm tra xem nếu xóa OWNER có phải cuối cùng ko
    if target_member.role == "OWNER":
        owner_count = db.query(SiteMemberModel).filter(
            SiteMemberModel.site_id == site_id,
            SiteMemberModel.role == "OWNER"
        ).count()

        if owner_count <=1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Không thể xóa chủ sở hữu (OWNER) cuối cùng của công trình."
            )

    db.delete(target_member)
    db.commit()

    # Hàm lưu lại lịch sử
    log_activity(db, user_id=current_user["user_id"], action="REMOVE_MEMBER", site_id=site_id, description=f"Đã xóa user_id {target_user_id} khỏi công trình")

    return {"detail": "Đã xóa thành viên khỏi công trình thành công."}

# Hàm xem danh sách thành viên trong công trình
def get_site_members_service(db:Session,site_id:int,current_user:dict):
    # Kiểm tra xem Công trình có tồn tại ko
    site = db.query(ConstructionSiteModel).filter(ConstructionSiteModel.id == site_id).first()

    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy công trình này"
        )

    # Kiểm tra xem có p thành viên của công trình
    is_member = db.query(SiteMemberModel).filter(
        SiteMemberModel.site_id == site_id,
        SiteMemberModel.user_id == current_user["user_id"]
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền xem danh sách thành viên của công trình này."
        )

    members = db.query(SiteMemberModel).filter(SiteMemberModel.site_id == site_id).all()

    return members

