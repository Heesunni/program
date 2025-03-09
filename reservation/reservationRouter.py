from typing import List
from fastapi import APIRouter, Depends, status
from common.response_wrapper import ResponseDto
from config.database import get_db
from sqlalchemy.orm import Session
from users.user import User
from reservation.dto.reservationRequest import UpsertReserveRequest
from reservation.dto.reservationResponse import ReserveIdResponse, ReserveListResponse
from reservation.reservationService import ReservationService
from middleware.getCurrentUserInfo import getCurrentUserInfo

router = APIRouter(
    tags=["reservation"],
    responses = {
        401 : {"description": "회원이 아님"},
        403 : {"description": "권한 없음"},
        404 : {"description": "특정 정보를 찾을 수 없음"},
        500 : {"description": "내부 에러"}
    },
    dependencies=[Depends(getCurrentUserInfo)]
)

#의존성 주입
def get_reserve_service(db: Session = Depends(get_db)) :
    return ReservationService(db)

##예약 조회
@router.get(
    "",
    name            = "예약 조회하기",
    status_code     = status.HTTP_200_OK,
    response_model  = ResponseDto[List[ReserveListResponse]]
)
def getReservationList(
    user: User = Depends(getCurrentUserInfo),
    reservationServie : ReservationService = Depends(get_reserve_service)
):
    result = reservationServie.getAllReservations(user)
    return ResponseDto( data = result)

##예약 신청
@router.post(
    "",
    name     = "예약 신청하기",
    status_code     = status.HTTP_200_OK,
    response_model  = ResponseDto[ReserveIdResponse]
)
def getReservation(
    req: UpsertReserveRequest,
    user: User = Depends(getCurrentUserInfo),
    reservationServie : ReservationService = Depends(get_reserve_service)
):
    result = reservationServie.createReservation(req, user)
    return ResponseDto( data = result)


##예약 수정
@router.put(
    "/{reserve_id}",
    name            = "예약 수정하기",
    status_code     = status.HTTP_200_OK,
    response_model  = ResponseDto[ReserveIdResponse]
)
def updateReservation(
    reservation_id: int,
    req: UpsertReserveRequest,
    user: User = Depends(getCurrentUserInfo),
    reservationServie : ReservationService = Depends(get_reserve_service)
):
    result = reservationServie.updateReservation( reservation_id, req, user)
    return ResponseDto( data = result)


##예약 확정
@router.patch(
    "/{reserve_id}/confirm",
    name            = "예약 확정하기",
    status_code     = status.HTTP_200_OK,
    response_model  = ResponseDto[ReserveIdResponse]
)
def confirmReservation(
    reservation_id: int,
    user: User = Depends(getCurrentUserInfo),
    reservationServie : ReservationService = Depends(get_reserve_service)
):
    result = reservationServie.confirmReservation( reservation_id, user)
    return ResponseDto( data = result)


##예약 삭제
@router.delete(
    "/{reserve_id}",
    name            = "예약 삭제하기(soft삭제지만, 직관성을위해 delete사용)",
    status_code     = status.HTTP_200_OK,
    response_model  = ResponseDto[ReserveIdResponse]
)
def deleteReservation(
    reservation_id: int,
    user: User = Depends(getCurrentUserInfo),
    reservationServie : ReservationService = Depends(get_reserve_service)
):
    result = reservationServie.deleteReservation( reservation_id, user)
    return ResponseDto( data = result)