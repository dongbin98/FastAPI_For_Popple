from src.models import User
from sqlalchemy.orm import Session
from src.domain.user.user_schemas import UserCreate, UserUpdate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 유저 목록 조회
def get_users(db: Session):
    user_list = db.query(User).all()
    return user_list


# 단일 유저 조회
def get_user(db: Session, user_id: int):
    user = db.query(User).get(user_id).first()
    return user


# 이미 가입된 계정 조회
def get_user_by_account(db: Session, account: str):
    user: User = db.query(User).filter(User.account == account).first()
    return user


# 유저 등록
def create_user(db: Session, user_create: UserCreate):
    user = User(account=user_create.account, password=pwd_context.hash(user_create.password), birth=user_create.birth,
                name=user_create.name,
                nickname=user_create.nickname, gps_agree=user_create.gps_agree, login_type=user_create.login_type,
                created_at=user_create.created_at, profile_image=user_create.profile_image)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# 유저 삭제
def delete_user(db: Session, user: User):
    db.delete(user)
    db.commit()


# 유저 갱신
def update_user(db: Session, user: User, user_update: UserUpdate):
    user.account = user_update.account
    user.password = user_update.password
    user.birth = user_update.birth
    user.name = user_update.name
    user.nickname = user_update.nickname
    user.gps_agree = user_update.gps_agree
    user.login_type = user_update.login_type
    user.profile_image = user_update.profile_image
    db.add(user)
    db.commit()
