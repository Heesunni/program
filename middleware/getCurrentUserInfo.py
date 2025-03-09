from fastapi import Depends, Request, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from users.userRepository import UserRepository
from users.user import User  # SQLAlchemy User 모델

##username으로 grade찾기
async def getCurrentUserInfo(
        username: str, db: Session = Depends(get_db)
) -> User:

    if not username:
        raise HTTPException(status_code=401 , detail="유저정보를 찾을 수 없습니다.")

    user_repository = UserRepository(db)
    user = user_repository.getUserbyUserName(username)

    if not user:
        raise HTTPException(status_code=401 , detail="유저정보를 찾을 수 없습니다.")

    return user