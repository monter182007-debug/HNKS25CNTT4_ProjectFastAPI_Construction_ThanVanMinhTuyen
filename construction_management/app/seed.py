from datetime import datetime
from db.database import SessionLocal
from core.security import hash_password
from models import UserModel,ConstructionSiteModel,SiteMemberModel,WorkItemModel

def seed_data():
    db= SessionLocal()

    try:
        if db.query(UserModel).first():
            print("Dữ liệu đã tồn tại trong Database")
            return

        admin_user = UserModel(
            email="admin@construction.com",
            password_hash=hash_password("hashed_password_123"),
            full_name="Quản trị viên Hệ thống",
            role="ADMIN",
            created_at=datetime.now()
        )

        normal_user = UserModel(
            email="ky_su_01@construction.com",
            password_hash=hash_password("hashed_password_456"),
            full_name="Kỹ sư Nguyễn Văn A",
            role="USER",
            created_at=datetime.now()
        )

        db.add_all([admin_user,normal_user])
        db.commit()
        db.refresh(admin_user)
        db.refresh(normal_user)


        # Tạo công trình
        site_1 = ConstructionSiteModel(
            name="Dự án Cầu Vượt Ngã Tư Sở",
            description="Thi công cầu vượt thép giảm ùn tắc giao thông",
            owner_id=admin_user.id,
            created_at=datetime.now()
        )
        db.add(site_1)
        db.commit()
        db.refresh(site_1)

        # Tạo thành viên
        member_1 = SiteMemberModel(
            site_id=site_1.id,
            user_id=normal_user.id,
            role="MEMBER",
            joined_at=datetime.now()
        )
        db.add(member_1)

        # Tạo hạng mục thi công
        work_1 = WorkItemModel(
            site_id=site_1.id,
            title="Đổ bê tông móng trụ T1",
            description="Đổ 500 khối bê tông mác 300 cho trụ chính",
            assignee_id=normal_user.id,
            status="IN_PROGRESS",
            priority="HIGH",
            due_date=datetime(2026, 12, 15),
            created_at=datetime.now()
        )
        db.add(work_1)
        db.commit()
        print("Đã nạp dữ liệu thành công")

    except Exception as e:
        print(f"Có lỗi xảy ra trong quá trình nạp dữ liệu: {e}")
        db.rollback()
    finally:
        db.close()
if __name__ == "__main__":
    seed_data()