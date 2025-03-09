from pydantic import BaseModel, Field
from typing import Any, Optional, Generic, TypeVar, Dict
from fastapi import status
from pydantic.generics import GenericModel

T = TypeVar("T")
class ResponseOkDto(BaseModel):
    status  : int           = Field(status.HTTP_200_OK, description="HTTP 상태 코드")


class ResponseDto(GenericModel, Generic[T]):
    status: int = Field(status.HTTP_200_OK, description="HTTP 상태 코드")
    data: Optional[T] = Field(None, description="응답 데이터")  # ✅ 제네릭 타입 적용
