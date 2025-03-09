from functools import wraps
from sqlalchemy.orm import Session
from fastapi import HTTPException
from config.database import get_db

def transactional(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        session: Session = next(get_db())
        try:
            with session.begin():
                kwargs["session"] = session
                result = func(self, *args, **kwargs)
                session.commit()
                return result
        except HTTPException as e:
            session.rollback()
            raise e
        except Exception as e:
            session.rollback()
            raise HTTPException(500, str(e))

    return wrapper

