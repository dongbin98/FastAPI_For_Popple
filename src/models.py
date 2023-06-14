import re
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Date, ForeignKey, Double
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import relationship, backref, declared_attr

# Example : One to One Relationship
# class Parent(Base):
#     __tablename__ = 'parent'
#     id = Column(Integer, primary_key=True)
#     child_id = Column(Integer, ForeignKey('child.id'))
#     child = relationship("Child", backref=backref("parent", uselist=False))
#
# class Child(Base):
#     __tablename__ = 'child'
#     id = Column(Integer, primary_key=True)
from src.database import Base


@as_declarative()
class Base:
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    __name__: str

    # CamelCase Class Name -> snake_case Table Name 자동생성
    @declared_attr
    def __tablename__(cls) -> str:
        return re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower()


class User(Base):
    id = Column(Integer, primary_key=True, index=True)  # 회원ID
    account = Column(String, nullable=False)  # 가입계정
    password = Column(String)  # 비밀번호
    birth = Column(DateTime)  # 생년월일
    name = Column(String, nullable=False)  # 이름
    nickname = Column(String)  # 닉네임
    login_type = Column(String, nullable=False)  # 로그인 타입
    profile_image = Column(String)  # 프로필사진

    user_type = Column(String)  # 유저 타입

    __mapper_args__ = {
        "polymorphic_on": user_type,
        "polymorphic_identity": "user",
    }
    # seller = relationship("Seller", backref=backref("user", uselist=False))  # User-Seller 1:1


class Seller(User):
    id = Column(Integer, ForeignKey("user.id"), primary_key=True)  # 셀러ID
    seller_name = Column(String, nullable=False)  # 셀러명
    insta_account = Column(String)  # 인스타 계정
    youtube_account = Column(String)  # 유튜브 계정
    website_url = Column(String)  # 웹사이트 주소
    seller_profile_image = Column(String)  # 프로필 사진

    __mapper_args__ = {
        "polymorphic_identity": "seller",
    }

    market = relationship("Market", backref="seller")  # Seller-Market 1:N
    seller_category = relationship("SellerCategory", backref="seller")


class SellerCategory(Base):
    id = Column(Integer, ForeignKey("seller.id"), primary_key=True)  # 셀러ID
    category_name = Column(String, nullable=False)  # 카테고리명


class Market(Base):
    id = Column(Integer, primary_key=True, index=True)  # 마켓ID
    name = Column(String, nullable=False)  # 마켓명
    open_date = Column(Date, nullable=False)  # 오픈날짜
    close_date = Column(Date, nullable=False)  # 마감날짜
    operation_status = Column(Boolean, nullable=False)  # 운영상태
    seller_id = Column(Integer, ForeignKey("seller.id"))  # 셀러ID

    market_type = Column(String)  # 마켓타입

    __mapper_args__ = {
        "polymorphic_on": market_type,
        "polymorphic_identity": "market",
    }


class PopupStore(Market):
    id = Column(Integer, ForeignKey("market.id"), primary_key=True)
    latitude = Column(Double, nullable=False)  # 위도
    longitude = Column(Double, nullable=False)  # 경도
    location = Column(String, nullable=False)  # 위치
    parking_lot = Column(Boolean, nullable=False)  # 주차장 여부
    toilet = Column(Boolean, nullable=False)  # 화장실 여부

    __mapper_args__ = {"polymorphic_identity": "popup_store", }


class FleeMarket(Market):
    id = Column(Integer, ForeignKey("market.id"), primary_key=True)
    event_id = Column(Integer, ForeignKey("event.id"))

    __mapper_args__ = {
        "polymorphic_identity": "flee_market",
    }


class Event(Base):
    id = Column(Integer, primary_key=True)  # 행사ID
    name = Column(String, nullable=False)  # 행사명
    latitude = Column(Double, nullable=False)  # 위도
    longitude = Column(Double, nullable=False)  # 경도
    location = Column(String, nullable=False)  # 위치
    parking_lot = Column(Boolean, nullable=False)  # 주차장 여부
    toilet = Column(Boolean, nullable=False)  # 화장실 여부

    flee_market = relationship("FleeMarket", backref="event")
