from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, BIGINT, DateTime, Boolean
from config.database import Base
from fastapi import HTTPException
__all__ = [
    "Reservation",
]

class Reservation(Base):
    __tablename__ = "reservation"
    id          = Column(BIGINT, autoincrement=True, primary_key=True, index=True)
    user_id     = Column(Integer, ForeignKey("users.id"))
    regnum      = Column(Integer, nullable=False)
    start_date  = Column(DateTime, nullable=False)
    end_date    = Column(DateTime, nullable=False)
    reg_date    = Column(DateTime, default=datetime.utcnow, nullable=False)
    confirmed   = Column(Boolean, default=False, nullable=False)
    canceled    = Column(Boolean, default=False, nullable=False)

    @classmethod
    def create(cls, user_id: int, start_date: datetime, end_date: datetime, regnum: int):
        return cls(
            user_id = user_id,
            start_date = start_date,
            end_date = end_date,
            regnum = regnum
        )

    def softDelete(self) :
        self.canceled = True
        return self

    def doConfirm(self) :
        self.confirmed = True
        return self

    def updateReservation(self, start_date: datetime, end_date: datetime, regnum: int):
        self.start_date = start_date
        self.end_date = end_date
        self.regnum = regnum
        return self


    @staticmethod
    def validate_before3date(start_date: datetime, end_date: datetime):
        MINDATE_DIFF = 3  # 최대 인원수

        # 신청일로부터 차이가 3일 이상인지 체크
        today = datetime.now().date()
        if ( start_date.date() - today).days < MINDATE_DIFF:
            raise HTTPException(400, "3일 후 날짜부터 선택 가능합니다.")

