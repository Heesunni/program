from datetime import datetime, timedelta
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, update, func, distinct
from common.enum import updateEnum
from config.database import get_db
from reservation.reservation import Reservation
from typing import Union, List, Optional

class ReservationRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    # 예약 생성
    def save(self, reservations: Reservation) -> Reservation:
        self.db.add(reservations)
        self.db.commit()
        self.db.refresh(reservations)  # DB에 반영된 최신 상태로 업데이트
        return reservations

    # 모든 삭제전 예약 조회
    def findAllValidReservations(self, uid: Optional[str] = None, reserve_id: Optional[str] = None) -> List[Reservation]:
        query = (
            select(Reservation)
            .where(Reservation.canceled == False)
        )

        if uid is not None:
            query = query.where(Reservation.user_id == uid)

        if reserve_id is not None:
            query = query.where(Reservation.id == reserve_id)

        result = self.db.execute(query)
        return result.scalars().all()

    # 특정 예약 상태 업데이트
    def update_reservation(self, reservation: Reservation) -> Reservation:
        data = vars(reservation).copy()
        data.pop("_sa_instance_state", None)

        query = (
            update(Reservation)
            .where(Reservation.id == reservation.id)
            .values(data)
            .returning(Reservation)
        )
        result = self.db.execute(query)
        self.db.commit()
        return result.scalar_one_or_none()

    # 특정 예약 조회
    def findOneReservationById(self, reserve_id: int, uid: Optional[str] = None, confirmed: Optional[bool] = None, needLock: Optional[bool] = False ) -> Union[Reservation, None]:
        query = (
            select(Reservation)
            .where(Reservation.id == reserve_id)
            .where(Reservation.canceled == False)
        )

        if uid is not None:
            query = query.where(Reservation.user_id == uid)

        if confirmed is not None:
            query = query.where(Reservation.confirmed == confirmed)

        ##for update lock걸기
        if needLock == True:
            query.with_for_update()

        result = self.db.execute(query)
        return result.scalars().first()


    # 특정 시간 동안의 예약 합계 조회
    def getSumReservationByHours(self, start_date: datetime, end_date: datetime, extract_reservid : Optional[int] == 0) -> int:

        query = (
            select(func.coalesce(func.sum(Reservation.regnum), 0))
            .where(Reservation.start_date < end_date)
            .where(Reservation.end_date > start_date)
            .where(Reservation.confirmed == True)
        )

        if extract_reservid > 0:
            query = query.where(Reservation.id != extract_reservid)

        result = self.db.execute(query)
        return result.scalars().first()
