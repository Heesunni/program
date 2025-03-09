from sqlalchemy import Column, String, Enum, BIGINT, Integer
from sqlalchemy.orm import declarative_base
from common.enum import GradeEnum
from config.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(BIGINT, primary_key=True, index=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)
    grade = Column( Integer, nullable=False)


    @classmethod
    def create(cls, username: str, grade: GradeEnum):
        return cls(username=username, grade=grade)

