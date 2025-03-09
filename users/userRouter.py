
from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBasic
from common.response_wrapper import ResponseDto, ResponseOkDto
from users.dto.userRequest import RegisterRequest
from users.userService import UserService
from config.database import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException
basic_auth = HTTPBasic()

router = APIRouter(
    tags=["auth"],
    responses = {
        400 : {"description": "이미 존재하는 username"},
        500 : {"description": "내부 에러"}
    }
)

#service의존성 주입
def get_user_service(db: Session = Depends(get_db)):
    return UserService(db)

## 유저 생성
@router.post(
    "/register",
    name            = "유저 집어넣고, 권한 부여하기",
    status_code     = status.HTTP_200_OK,
    response_model  = ResponseOkDto
)
def register(
        req : RegisterRequest,
        userService : UserService = Depends(get_user_service)
    ):
        userService.register( req.username, req.grade)
        return ResponseOkDto()
