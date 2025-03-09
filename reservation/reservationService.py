from typing import List
from sqlalchemy.orm import Session
from common.enum import GradeEnum
from .dto.reservationRequest import UpsertReserveRequest
from .dto.reservationResponse import ReserveIdResponse, ReserveListResponse
from .reservation import Reservation
from .reservationRepository import ReservationRepository
from users.user import User
from fastapi import HTTPException

class ReservationService:
    def __init__(self, db: Session):
        self.db = db
        self.reservationRepository = ReservationRepository(db)

    def getAllReservations(self, user: User) -> List[ReserveListResponse]:

        ## 예약정보 가져오기( 권한에 따라 분류)
        reservations: List[Reservation] = []

        # 어드민은 모든예약 조회
        if user.grade == GradeEnum.ADMIN:
            reservations = self.reservationRepository.findAllValidReservations()

        # 일반유저는 본인의 것에 한에서만 확정전에 업데이트 가능
        else:
            reservations = self.reservationRepository.findAllValidReservations( uid= user.id)

        result = [ReserveListResponse.from_reservation(res) for res in reservations]
        return result


    def createReservation(self, req: UpsertReserveRequest, user: User):
        try:
            Reservation.validate_date(start_date=req.start_date, end_date=req.end_date)
            self.validate_maxcnt(req)
            
            # 예약 생성하기
            new_reservation = Reservation.create(
                start_date = req.start_date,
                end_date = req.end_date,
                user_id = user.id,
                regnum = req.regnum
            )

            result = self.reservationRepository.save(new_reservation)
            return ReserveIdResponse( id = result.id)

        except HTTPException as e:
            raise e

        except Exception as e:
            raise HTTPException(500, str(e))

    def updateReservation(self, reserve_id: int, req: UpsertReserveRequest, user: User):
        try:
            reservation: Reservation

            ## 예약정보 가져오기( 권한에 따라 분류)
            # 어드민은 모든예약 업데이트 가능
            if user.grade == GradeEnum.ADMIN:
                reservation = self.reservationRepository.findOneReservationById(
                    reserve_id = reserve_id
                )

            # 일반유저는 본인의 것에 한에서만 확정전에 업데이트 가능
            else:
                reservation = self.reservationRepository.findOneReservationById(
                    reserve_id = reserve_id,
                    uid = user.id,
                    confirmed = False
                )

            if reservation == None:
                raise HTTPException(404, "수정가능한 예약정보가 없습니다.")

            ## validation check
            Reservation.validate_date(start_date=req.start_date, end_date=req.end_date)
            self.validate_maxcnt(req)


            # 예약 수정하기
            reservation = reservation.updateReservation(
                start_date = req.start_date,
                end_date = req.end_date,
                regnum = req.regnum
            )

            result = self.reservationRepository.update_reservation(reservation= reservation)
            return ReserveIdResponse( id = result.id)

        except HTTPException as e:
            raise e

        except Exception as e:
            raise HTTPException(500, str(e))

    def deleteReservation(self, reserve_id: int, user: User):
        try:
            ## 예약정보 가져오기( 권한에 따라 분류)
            # 어드민은 모든예약 삭제 가능
            if user.grade == GradeEnum.ADMIN:
                reservation = self.reservationRepository.findOneReservationById(
                    reserve_id = reserve_id
                )

            # 일반유저는 본인의 것에 한에서만 확정전에 삭제가능
            else:
                reservation = self.reservationRepository.findOneReservationById(
                    reserve_id = reserve_id,
                    uid = user.id,
                    confirmed = False
                )

            if reservation == None:
                raise HTTPException(404, "삭제가능한 예약정보가 없습니다.")


            ##예약 취소하기
            reservation = reservation.softDelete()
            result = self.reservationRepository.update_reservation(reservation= reservation)
            return ReserveIdResponse( id = result.id)

        except HTTPException as e:
            raise e

        except Exception as e:
            raise HTTPException(500, str(e))

    def confirmReservation(self, reserve_id: int, user: User):
        try:
            # 어드민만 예약 확정 가능
            if user.grade != GradeEnum.ADMIN:
                raise HTTPException(403, "권한이 없습니다.")

            if user.grade == GradeEnum.ADMIN:
                reservation = self.reservationRepository.findOneReservationById(
                    reserve_id = reserve_id,
                    confirmed = False
                )

            if reservation == None:
                raise HTTPException(404, "확정가능한 예약정보가 없습니다.")

            ##확정가능한지 인원수 카운트
            self.validate_maxcnt(UpsertReserveRequest(
                start_date = reservation.start_date,
                end_date = reservation.end_date,
                regnum = reservation.regnum
            ))

            ##예약 확정하기
            reservation = reservation.doConfirm()
            result = self.reservationRepository.update_reservation(reservation= reservation)
            return ReserveIdResponse( id = result.id)

        except HTTPException as e:
            raise e

        except Exception as e:
            raise HTTPException(500, str(e))

    def validate_maxcnt(self, req: UpsertReserveRequest):
        MAXCNT = 50000  # 최대 인원수

        # 해당 기간에 신청 가능한 인원수 체크
        current_count = self.reservationRepository.getSumReservationByHours(
            start_date=req.start_date,
            end_date=req.end_date
        )

        if current_count + req.regnum > MAXCNT:
            raise HTTPException(400, "해당 기간에는 더 이상 신청할 수 없습니다.")