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
from schemas.comment import CommentCreate,CommentResponse
from services.comment import create_comment_service,get_comments_service


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


# API tạo comment cho hạng mục thi công
@router.post("/{work_item_id}/comments",response_model=CommentResponse,status_code=status.HTTP_201_CREATED)
def create_comment(
    work_item_id:int,
    comment_data:CommentCreate,
    db:Session = Depends(get_db),
    current_user:dict = Depends(get_current_user)
):
    return create_comment_service(db=db, work_item_id=work_item_id, comment_data=comment_data, current_user=current_user)

# API xem comment cho hạng mục thi công
@router.get("/{work_item_id}/comments",response_model=List[CommentResponse],status_code=status.HTTP_200_OK)
def get_comments(
    work_item_id:int,
    db:Session =Depends(get_db),
    current_user:dict = Depends(get_current_user)
):
    return get_comments_service(db=db, work_item_id=work_item_id, current_user=current_user)