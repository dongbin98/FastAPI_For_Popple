from fastapi import APIRouter, Depends, Query, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.domain.seller import seller_schemas
from src.domain.seller import seller_crud
from src.database import get_db

router = APIRouter(
    prefix="/api/seller"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")


@router.get("/list", response_model=list[seller_schemas.Seller])
def read_sellers(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):  # 의존성 주입
    _seller_list = seller_crud.get_sellers(db)
    return _seller_list


# 이미 등록된 셀러명 조회
@router.get("/name", response_model=seller_schemas.Seller)
async def check_seller_name(name: str = Query(default=None), db: Session = Depends(get_db)):
    seller = seller_crud.get_seller_by_name(db, name)
    if not seller:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not assigned Nickname",
        )
    else:
        return seller


# 셀러 등록
@router.post("/add", status_code=status.HTTP_200_OK)
async def create_seller(seller_create: seller_schemas.SellerCreate, db: Session = Depends(get_db)):
    return seller_crud.create_seller(db, seller_create)


# 셀러 카테고리 등록
@router.post("/add/category", status_code=status.HTTP_200_OK)
async def create_seller_category(seller_category_create: seller_schemas.SellerCategoryCreate, db: Session = Depends(get_db)):
    return seller_crud.create_seller_category(db, seller_category_create)