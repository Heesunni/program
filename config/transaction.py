from functools import wraps
from sqlalchemy.orm import Session
from fastapi import HTTPException
from config.database import get_db  # ✅ DB 세션을 가져오는 함수

def transactional(func):
    """Spring의 @Transactional과 유사한 기능을 제공하는 데코레이터"""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        session: Session = next(get_db())  # ✅ Generator에서 실제 Session 객체 가져오기
        try:
            with session.begin():  # ✅ 트랜잭션 시작
                kwargs["session"] = session  # ✅ session을 kwargs에 추가
                result = func(self, *args, **kwargs)  # ✅ session을 인자로 전달하지 않고 kwargs로 넘김
                session.commit()  # ✅ 트랜잭션 커밋
                return result
        except HTTPException as e:
            session.rollback()  # ❌ 예외 발생 시 롤백
            raise e
        except Exception as e:
            session.rollback()  # ❌ 기타 예외 발생 시 롤백
            raise HTTPException(500, str(e))

    return wrapper

