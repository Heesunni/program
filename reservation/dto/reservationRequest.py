from pydantic import BaseModel, Field, field_validator
from datetime import datetime

class UpsertReserveRequest(BaseModel):
    start_date : datetime = Field(..., description="예약 시작날짜 및 시간(YYYY-MM-DD HH)", example='2025-04-01 13:00')
    end_date : datetime = Field(..., description="예약 종료날짜 및 시간(YYYY-MM-DD HH)", example='2025-04-01 15:00')
    regnum : int = Field(..., ge=1, description="응시 인원 (최소 1명 이상)")
    @field_validator("end_date", mode="after")
    @classmethod
    def check_valid_time(cls, end_date: datetime, values: dict):
        """start_date가 end_date보다 크면 에러 발생"""
        print("=========")
        print(values)
        start_date = values.data["start_date"]

        if start_date and end_date and start_date >= end_date:
            raise ValueError("시작시간이 종료시간보다 클 수 없습니다.")

        return end_date

    class Config:
        orm_mode = True

