from src.domain.seller.seller_schemas import SellerCreate, SellerCategoryCreate
from src.models import Seller, SellerCategory
from sqlalchemy.orm import Session


# 셀러 목록 조회
def get_sellers(db: Session):
    seller_list = db.query(Seller).all()
    return seller_list


# 단일 셀러 조회
def get_seller(db: Session, seller_id: int):
    seller = db.query(Seller).filter(Seller.id == seller_id)
    return seller


# 이미 등록된 셀러명 조회
def get_seller_by_name(db: Session, name: str):
    seller: Seller = db.query(Seller).filter(Seller.name == name).first()
    return seller


# 셀러 등록
def create_seller(db: Session, seller_create: SellerCreate):
    seller = Seller(seller_name=seller_create.seller_name, insta_account=seller_create.insta_account,
                    youtube_account=seller_create.youtube_account, website_url=seller_create.website_url,
                    seller_profile_image=seller_create.seller_profile_image)
    db.add(seller)
    db.commit()
    db.refresh(seller)
    return seller


# 셀러 카테고리 등록
def create_seller_category(db: Session, seller_category: SellerCategoryCreate):
    seller_category = SellerCategory(id=seller_category.id, category_name=seller_category.category_name)

    db.add(seller_category)
    db.commit()
    db.refresh(seller_category)
    return seller_category
