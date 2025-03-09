from __future__ import annotations
from sqlalchemy import select
from fastapi import Depends
from sqlalchemy.orm import Session
from config.database import get_db
from users.user import User


class UserRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def save(self, user: User) -> None:
        self.db.add(user)
        self.db.commit()

    def getUserbyUserName(self, username: str) -> User | None:
        result = self.db.execute(select(User).where(User.username == username))
        return result.scalars().first()