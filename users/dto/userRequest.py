from pydantic import BaseModel
from common.enum import GradeEnum
from pydantic import  Field
class RegisterRequest(BaseModel):
     username  : str       = Field(..., description='유저아이디', example='user1')
     grade     : GradeEnum = Field(..., description=' 0 : 어드민, 1: 일반 유저')

     class Config:
          orm_mode = True
