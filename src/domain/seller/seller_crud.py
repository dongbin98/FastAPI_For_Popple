from src.models import User
from sqlalchemy.orm import Session
from src.domain.seller.seller_schemas import *


def get_users(db: Session):
    user_list = db.query(User).all()
    return user_list


def get_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id)
    return user


def get_user_by_account(db: Session, account: str):
    return db.query(User).filter(User.account == account).first()