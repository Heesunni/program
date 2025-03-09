from fastapi import FastAPI,Depends
from users.userRouter import router as UserRouter
from reservation.reservationRouter import router as reservationsRouter
from config.database import engine, Base


app = FastAPI()

# Base.metadata.drop_all(bind=engine) #db 테이블초기화
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")

app.include_router( UserRouter, prefix="/user")
app.include_router( reservationsRouter, prefix="/reservation/{username}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
