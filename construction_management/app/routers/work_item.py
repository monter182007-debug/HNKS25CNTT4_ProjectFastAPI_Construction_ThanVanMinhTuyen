from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session
from typing import List
from db.database import get_db
from dependencies.auth import get_current_user
from schemas.work_item import WorkItemCreate, WorkItemResponse,WorkItemUpdate
from services.work_item import (
    get_work_item_detail_service,
    update_update_work_item_service,
    delete_work_item_service
)

router = APIRouter(prefix="/work-items", tags=["Work Items"])

# API xem chi tiết hạng mục thi công
@router.get("/{item_id}", response_model=WorkItemResponse, status_code=status.HTTP_200_OK)
def get_work_item_detail(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return get_work_item_detail_service(db=db, work_item_id=item_id, current_user=current_user)

# API cập nhật hạng mục thi công
@router.patch("/{item_id}",response_model=WorkItemResponse,status_code=status.HTTP_200_OK)
def update_work_item(
    item_id:int,
    item_data:WorkItemUpdate,
    db:Session = Depends(get_db),
    current_user:dict = Depends(get_current_user)
):
    return update_update_work_item_service(db=db, work_item_id=item_id, item_data=item_data, current_user=current_user)


# API xóa hạng mục thi công
@router.delete("/{item_id}", status_code=status.HTTP_200_OK)
def delete_work_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return delete_work_item_service(db=db, work_item_id=item_id, current_user=current_user)