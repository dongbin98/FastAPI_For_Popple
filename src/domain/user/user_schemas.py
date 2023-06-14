import datetime
from pydantic import BaseModel


# 유저 기본 스키마
class User(BaseModel):
    id: int
    account: str
    password: str | None = None
    birth: datetime.date | None = None
    name: str
    nickname: str | None = None
    login_type: str
    profile_image: str | None = None

    class Config:
        orm_mode = True


# 회원가입 스키마
class UserCreate(BaseModel):
    account: str
    password: str
    birth: datetime.date
    name: str
    nickname: str
    login_type: str
    profile_image: str | None = None

    # 추후 검색해보자
    # @validator('account', 'password', 'birth', 'name', 'nickname', 'gps_agree', 'login_type', 'created_at')
    # def not_empty(cls, v):
    #     if not v or not v:
    #         raise ValueError('빈 값은 허용되지 않습니다.')
    #     return v


# 회원가입 with 네이버 스키마
class UserCreateWithNaver(BaseModel):
    account: str
    password: str
    birth: datetime.date
    name: str
    nickname: str
    login_type: str
    profile_image: str | None = None


# 회원가입 with 카카오 스키마
class UserCreateWithKakao(BaseModel):
    account: str
    password: str
    name: str
    login_type: str
    profile_image: str | None = None


# # SSO 로그인 스키마
# class LoginWithSSO(BaseModel):
#     account: str


# access_token 스키마
class Token(BaseModel):
    access_token: str
    token_type: str
    username: str


class UserUpdate(UserCreate):
    user_id: int


class UserDelete(BaseModel):
    user_id: int
