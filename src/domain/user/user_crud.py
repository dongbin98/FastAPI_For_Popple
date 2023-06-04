from src.models import User
from sqlalchemy.orm import Session
from src.domain.user.user_schemas import UserCreate, UserCreateWithNaver, UserCreateWithKakao, UserUpdate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 유저 목록 조회
def get_users(db: Session):
    user_list = db.query(User).all()
    return user_list


# 단일 유저 조회
def get_user(db: Session, user_id: int):
    user: User = db.query(User).filter(User.id == user_id).first()
    return user


# 이미 가입된 계정 조회
def get_user_by_account(db: Session, account: str):
    user: User = db.query(User).filter(User.account == account).first()
    return user


# 이미 등록된 닉네임 조회
def get_user_by_nickname(db: Session, nickname: str):
    user: User = db.query(User).filter(User.nickname == nickname).first()
    return user


# 유저 등록
def create_user(db: Session, user_create: UserCreate):
    user = User(account=user_create.account, password=pwd_context.hash(user_create.password), birth=user_create.birth,
                name=user_create.name, nickname=user_create.nickname, login_type=user_create.login_type,
                created_at=user_create.created_at, profile_image=user_create.profile_image)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# 유저 등록 with Naver
def create_user_with_naver(db: Session, user_create: UserCreateWithNaver):
    user = User(account=user_create.account,  birth=user_create.birth,
                name=user_create.name, nickname=user_create.nickname, login_type=user_create.login_type,
                created_at=user_create.created_at, profile_image=user_create.profile_image)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# 유저 등록 with Kakao
def create_user_with_kakao(db: Session, user_create: UserCreateWithKakao):
    user = User(account=user_create.account,  name=user_create.name, login_type=user_create.login_type,
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
    user.login_type = user_update.login_type
    user.profile_image = user_update.profile_image
    db.add(user)
    db.commit()
