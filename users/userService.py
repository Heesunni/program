from fastapi import HTTPException
from common.enum import GradeEnum
from users.user import User
from users.userRepository import UserRepository
from sqlalchemy.orm import Session

class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.userRepository = UserRepository(db)

    def register( self, username : str, grade: GradeEnum):
        try:
            if self.userRepository.getUserbyUserName(username):
                raise HTTPException( 400, "이미 존재하는 유저이름입니다.")

            newUser = User.create(username = username, grade = grade)
            self.userRepository.save(user = newUser)

        except HTTPException as e:
            raise e

        except Exception as e:
            raise HTTPException(500, str(e))





