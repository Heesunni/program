
from enum import IntEnum

# 응답코드 enum
class StatusEnum(IntEnum):
    OK = 200
    ERROR = 400


# 권한 enum
class GradeEnum(IntEnum):
    ADMIN = 0
    USER  = 1


class updateEnum(IntEnum):
    INIT   = 0
    CANCEL = 1
    OK     = 2



# class ErrorEnum(enum):
#     400 = "이미 존재하는 유저이름입니다."
#     404 = "유저정보를 찾을 수 없습니다."
#
