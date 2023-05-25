from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite in Project Root Directory
# SQLALCHEMY_DATABASE_URL = "sqlite:///./myapi.db"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:!ytskjs173@localhost/popple"

# Set Connection Pool
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # 사용한 세션을 커넥션 풀에 반환, 세션 종료 아님
