from pydantic import BaseModel


# 셀러 기본 스키마
class Seller(BaseModel):
    id: int
    seller_name: str
    insta_account: str | None = None
    youtube_account: str | None = None
    website_url: str | None = None
    seller_profile_image: str | None = None

    class Config:
        orm_mode = True


# 셀러 카테고리 스키마
class SellerCategory(BaseModel):
    id: int
    category_name: str

    class Config:
        orm_mode = True


# 셀러 등록 스키마
class SellerCreate(BaseModel):
    id: int
    seller_name: str
    insta_account: str | None = None
    youtube_account: str | None = None
    website_url: str | None = None
    seller_profile_image: str | None = None


# 셀러 카테고리 스키마
class SellerCategoryCreate(BaseModel):
    id: int
    category_name: str


class SellerUpdate(SellerCreate):
    seller_id: int


class SellerDelete(BaseModel):
    seller_id: int
