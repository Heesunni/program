from fastapi import FastAPI,Depends
from users.userRouter import router as UserRouter
from reservation.reservationRouter import router as reservationsRouter
from config.database import engine, Base


app = FastAPI()

# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")

app.include_router( UserRouter, prefix="/user")
app.include_router( reservationsRouter, prefix="/reservation/{username}")

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


