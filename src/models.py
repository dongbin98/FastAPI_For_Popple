from sqlalchemy import Column, Integer, String, DateTime, TIMESTAMP, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)  # 회원ID
    account = Column(String, nullable=False)  # 가입계정
    password = Column(String, nullable=False)  # 비밀번호
    birth = Column(DateTime, nullable=False)  # 생년월일
    name = Column(String, nullable=False)  # 이름
    nickname = Column(String, nullable=False)  # 닉네임
    gps_agree = Column(Boolean, nullable=False)  # GPS 동의여부
    login_type = Column(String, nullable=False)  # 로그인 타입
    created_at = Column(DateTime, nullable=False)  # 가입일자
    profile_image = Column(String)  # 프로필사진


class Seller(Base):
    __tablename__ = "seller"

    id = Column(Integer, ForeignKey("user.id"), primary_key=True)  # 셀러ID
    seller_name = Column(String, nullable=False)  # 셀러명
    insta_account = Column(String)  # 인스타 계정
    youtube_account = Column(String)  # 유튜브 계정
    website_url = Column(String)  # 웹사이트 주소
    profile_image = Column(String)  # 프로필 사진

    markets = relationship("Market", back_populates="owner")


class Market(Base):
    __tablename__ = "market"

    id = Column(Integer, primary_key=True)  # 마켓ID
    name = Column(String, nullable=False)  # 마켓명
    open_date = Column(Date, nullable=False)  # 오픈날짜
    close_date = Column(Date, nullable=False)  # 마감날짜
    operation_status = Column(Boolean, nullable=False)  # 운영상태
    seller_id = Column(Integer, ForeignKey("seller.id"))  # 셀러ID

    owner = relationship("Seller", back_populates="markets")
