from datetime import datetime
from typing import Type

from pydantic import BaseModel
from pydantic import  Field


class ReserveIdResponse(BaseModel):
    id  : int  = Field( ..., description='예약id')
    class Config:
        orm_mode = True


class ReserveListResponse(BaseModel):
    id: int = Field(None, description="예약 ID")
    user_id: int = Field(None, description="신청 유저 uid")
    regnum: int = Field(..., description="응시 인원")
    start_date: datetime = Field(..., description="예약 시작날짜 및 시간 (YYYY-MM-DD HH)", example="2025-04-01 13:00")
    end_date: datetime = Field(..., description="예약 종료날짜 및 시간 (YYYY-MM-DD HH)", example="2025-04-01 15:00")
    reg_date: datetime = Field(..., description="예약 등록 날짜")
    confirmed: bool = Field(default=False, description="예약 확정 여부")

    @classmethod
    def from_reservation(cls: Type["ReserveListResponse"], reservation: "Reservation") -> "ReserveListResponse":
        return cls(
            id = reservation.id,
            user_id = reservation.user_id,
            regnum = reservation.regnum,
            start_date = reservation.start_date,
            end_date = reservation.end_date,
            reg_date = reservation.reg_date,
            confirmed = reservation.confirmed
        )

    class Config:
        from_attributes = True
