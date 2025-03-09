from pydantic import BaseModel, Field
from datetime import datetime

class UpsertReserveRequest(BaseModel):
    start_date : datetime = Field(..., description="예약 시작날짜 및 시간(YYYY-MM-DD HH)", example='2025-04-01 13:00')
    end_date : datetime = Field(..., description="예약 종료날짜 및 시간(YYYY-MM-DD HH)", example='2025-04-01 15:00')
    regnum : int = Field(..., ge=1, description="응시 인원 (최소 1명 이상)")

    class Config:
        orm_mode = True

