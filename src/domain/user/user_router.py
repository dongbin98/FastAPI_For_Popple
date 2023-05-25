from datetime import timedelta, datetime

from fastapi import APIRouter, Depends, status
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from src.database import get_db
from src.domain.user import user_schemas, user_crud
from src.domain.user.user_crud import pwd_context
from src.models import User

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY = "416110369e15917a95ef9ac031368e911a47e18c7e70d5b42056193b6d02477f"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")

router = APIRouter(
    prefix="/api/user"
)


def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_account: str = payload.get("sub")
        if user_account is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        user = user_crud.get_user_by_account(db, account=user_account)
        if user is None:
            raise credentials_exception
        return user


@router.post("/login", response_model=user_schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 아이디 및 패스워드 체크
    user = user_crud.get_user_by_account(db, form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect account or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # access_token 생성
    data = {
        "sub": user.account,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.account
    }


# 유저 목록 조회
@router.get("/list", response_model=list[user_schemas.User])
def read_users(db: Session = Depends(get_db)):  # 의존성 주입
    _user_list = user_crud.get_users(db=db)
    return _user_list


# 단일 유저 조회
@router.get("/{user_id}", response_model=user_schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = user_crud.get_user(db=db, user_id=user_id)
    return user


# 유저 등록
@router.post("/add", status_code=status.HTTP_200_OK)
def create_user(user_create: user_schemas.UserCreate, db: Session = Depends(get_db)):
    # 이메일로 중복 가입 방지
    db_user = user_crud.get_user_by_account(db, user_create.account)
    if db_user:
        raise HTTPException(status_code=400, detail="이미 존재하는 계정입니다.")
    return user_crud.create_user(db, user_create)


# 유저 삭제
@router.delete("/delete/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(_user_delete: user_schemas.UserDelete, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    _user = user_crud.get_user(db, user_id=_user_delete.user_id)
    if not _user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="데이터를 찾을 수 없습니다")
    if current_user.id != _user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="삭제 권한이 없습니다")
    return user_crud.delete_user(db=db, user=_user)


# 유저 갱신
@router.put("/update", status_code=status.HTTP_200_OK)
def update_user(_user_update: user_schemas.UserUpdate, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    _user = user_crud.get_user(db, user_id=_user_update.user_id)
    if not _user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="데이터를 찾을 수 없습니다")
    if current_user.id != _user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="수정 권한이 없습니다")
    user_crud.update_user(db, user=_user, user_update=_user_update)
