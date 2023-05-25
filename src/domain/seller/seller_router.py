from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.domain.seller import seller_schemas
from src.domain.seller import seller_crud
from src.database import get_db

router = APIRouter(
    prefix="/api/user"
)


@router.get("/list", response_model=list[seller_schemas.User])
def read_users(db: Session = Depends(get_db)):  # 의존성 주입
    _user_list = seller_crud.get_users(db)
    return _user_list


# @router.get("/info", response_model=schemas.User)
# def read_user(db: Session = Depends(get_db())):
#     _user = user_crud.get_user(db, 1)
#     return _user
