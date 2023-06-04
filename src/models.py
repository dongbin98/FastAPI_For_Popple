from sqlalchemy import Column, Integer, String, DateTime, Boolean, Date, ForeignKey, Double
from sqlalchemy.orm import relationship, backref
from src.database import Base


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


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)  # 회원ID
    account = Column(String, nullable=False)  # 가입계정
    password = Column(String)  # 비밀번호
    birth = Column(DateTime)  # 생년월일
    name = Column(String, nullable=False)  # 이름
    nickname = Column(String)  # 닉네임
    login_type = Column(String, nullable=False)  # 로그인 타입
    created_at = Column(DateTime, nullable=False)  # 가입일자
    profile_image = Column(String)  # 프로필사진

    seller = relationship("Seller", backref=backref("user", uselist=False))  # User-Seller 1:1


class Seller(User):
    __tablename__ = "seller"
    id = Column(Integer, ForeignKey("user.id"), primary_key=True)  # 셀러ID
    seller_name = Column(String, nullable=False)  # 셀러명
    insta_account = Column(String)  # 인스타 계정
    youtube_account = Column(String)  # 유튜브 계정
    website_url = Column(String)  # 웹사이트 주소
    seller_profile_image = Column(String)  # 프로필 사진

    market = relationship("Market", backref="seller")  # Seller-Market 1:N


class Market(Base):
    __tablename__ = "market"
    id = Column(Integer, primary_key=True)  # 마켓ID
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
    __tablename__ = "popup_store"
    id = Column(Integer, ForeignKey("market.id"), primary_key=True)
    latitude = Column(Double, nullable=False)  # 위도
    longitude = Column(Double, nullable=False)  # 경도
    location = Column(String, nullable=False)  # 위치
    parking_lot = Column(Boolean, nullable=False)  # 주차장 여부
    toilet = Column(Boolean, nullable=False)  # 화장실 여부

    __mapper_args__ = {"polymorphic_identity": "popup_store", }


class FleeMarket(Market):
    __tablename__ = "flee_market"
    id = Column(Integer, ForeignKey("market.id"), primary_key=True)
    event_id = Column(Integer, ForeignKey("event.id"))

    __mapper_args__ = {
        "polymorphic_identity": "flee_market",
    }


class Event(Base):
    __tablename__ = "event"
    id = Column(Integer, primary_key=True)  # 행사ID
    name = Column(String, nullable=False)  # 행사명
    latitude = Column(Double, nullable=False)  # 위도
    longitude = Column(Double, nullable=False)  # 경도
    location = Column(String, nullable=False)  # 위치
    parking_lot = Column(Boolean, nullable=False)  # 주차장 여부
    toilet = Column(Boolean, nullable=False)  # 화장실 여부

    flee_market = relationship("FleeMarket", backref="event")
