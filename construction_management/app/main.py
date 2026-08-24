from fastapi import FastAPI
from db.database import Base,engine
from models import UserModel,UserModel, ConstructionSiteModel, SiteMemberModel, WorkItemModel,ActivityLogModel
from core.exceptions import get_exception_handlers
from routers import auth,users,construction,work_item
# Tạo bảng trong database
Base.metadata.create_all(bind=engine)

app = FastAPI(exception_handlers=get_exception_handlers())
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(construction.router)
app.include_router(work_item.router)
# API kiểm tra server
@app.get("/")
def read_root():
    return {"message": "Hệ thống API đã khởi động thành công!"}