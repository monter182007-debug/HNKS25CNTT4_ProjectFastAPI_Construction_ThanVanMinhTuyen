from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from db.database import get_db
from dependencies.auth import get_current_user
from models.user import UserModel
from schemas.site import (
    ConstructionSiteCreate,
    ConstructionSiteResponse,
    SiteMemberResponse,
    SiteMemberCreate)
from schemas.work_item import (WorkItemCreate,WorkItemResponse)
from services.construction import (
    create_construction_site_service,
    get_user_construction_sites_service,
    get_construction_site_detail_service,
    update_construction_site_service,
    delete_construction_site_service,
    add_site_member_service,
    remove_site_member_service,
    get_site_members_service)
from services.work_item import create_work_item_service,get_work_item_detail_service,get_work_items_service
from typing import Optional,List

router = APIRouter(prefix="/construction-sites", tags=["Construction Sites"])

# API thêm mới công trình
@router.post("/",response_model=ConstructionSiteResponse,status_code=status.HTTP_201_CREATED)
def create_construction_site(
    site_data:ConstructionSiteCreate,
    db:Session = Depends(get_db),
    current_user:dict = Depends(get_current_user)
):
    return create_construction_site_service(db,site_data,current_user)

# API xem danh sách công trình 
@router.get("/",response_model=List[ConstructionSiteResponse])
def get_construction_sites(
    search:Optional[str] = None,
    db:Session = Depends(get_db),
    current_user:dict = Depends(get_current_user)
):
    return get_user_construction_sites_service(db=db, current_user=current_user, search=search)

# API xem chi tiết công trình
@router.get("/{site_id}",response_model=ConstructionSiteResponse)
def get_construction_site_detail(
    site_id:int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return get_construction_site_detail_service(db=db, site_id=site_id, current_user=current_user)

# API cập nhật công trình
@router.put("/{site_id}",response_model=ConstructionSiteResponse)
def update_site(
    site_id:int,
    site_data:ConstructionSiteCreate,
    db:Session = Depends(get_db),
    current_user:dict = Depends(get_current_user)
):
    return update_construction_site_service(db, site_id, site_data, current_user)

# API xóa công trình
@router.delete("/{site_id}")
def delete_site(site_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return delete_construction_site_service(db, site_id, current_user)

# API thêm mới thành viên công trình 
@router.post("/{site_id}/members",response_model=SiteMemberResponse,status_code=status.HTTP_201_CREATED)
def add_site_member(
    site_id:int,
    member_data:SiteMemberCreate,
    db:Session = Depends(get_db),
    current_user:dict = Depends(get_current_user)
):
    return add_site_member_service(db=db, site_id=site_id, member_data=member_data, current_user=current_user)

# API xóa thành viên khỏi công trình
@router.delete("/{site_id}/members/{target_user_id}")
def remove_site_member(
    site_id:int,
    target_user_id:int,
    db:Session = Depends(get_db),
    current_user:dict = Depends(get_current_user)
):
    return remove_site_member_service(db,site_id,target_user_id,current_user)

# API xem danh sách thành viên công trình
@router.get("/{site_id}/members",response_model=list[SiteMemberResponse])
def get_site_members(
    site_id:int,
    db:Session = Depends(get_db),
    current_user:dict = Depends(get_current_user)
):
    return get_site_members_service(db,site_id,current_user)

# API thêm hạng mục thi công
@router.post("/{site_id}/work-items", response_model=WorkItemResponse, status_code=status.HTTP_201_CREATED)
def create_work_item(
    site_id: int,
    item_data: WorkItemCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return create_work_item_service(db=db, site_id=site_id, item_data=item_data, current_user=current_user)

# Hàm xem danh sách các hạng mục thi công 
@router.get("/{site_id}/work-items", response_model=List[WorkItemResponse], status_code=status.HTTP_200_OK)
def get_work_items(
    site_id: int,
    statuss: Optional[str] = None,
    priority: Optional[str] = None,
    assignee_id: Optional[int] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 1,
    sort_by: str = "created_at",
    order: str = "desc",
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return get_work_items_service(
      db=db, 
        site_id=site_id, 
        current_user=current_user,
        statuss=statuss,
        priority=priority,
        assignee_id=assignee_id,
        search=search,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        order=order)