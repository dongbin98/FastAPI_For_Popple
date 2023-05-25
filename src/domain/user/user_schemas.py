import datetime
from pydantic import BaseModel, validator


class User(BaseModel):
    id: int
    account: str
    password: str
    birth: datetime.datetime
    name: str
    nickname: str
    gps_agree: bool
    login_type: str
    created_at: datetime.datetime
    profile_image: str | None = None

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    account: str
    password: str
    birth: datetime.datetime
    name: str
    nickname: str
    gps_agree: bool
    login_type: str
    created_at: datetime.datetime
    profile_image: str | None = None

    # 추후 검색해보자
    # @validator('account', 'password', 'birth', 'name', 'nickname', 'gps_agree', 'login_type', 'created_at')
    # def not_empty(cls, v):
    #     if not v or not v:
    #         raise ValueError('빈 값은 허용되지 않습니다.')
    #     return v


class Token(BaseModel):
    access_token: str
    token_type: str
    username: str


class UserUpdate(UserCreate):
    user_id: int


class UserDelete(BaseModel):
    user_id: int
