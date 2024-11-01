from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

# واردات از پکیج‌های محلی
from api import models, schemas
from api.database import engine, Base, get_db

app = FastAPI()

# ایجاد جداول در دیتابیس
Base.metadata.create_all(bind=engine)

@app.post("/api/user", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(
        firstName=user.firstName,
        lastName=user.lastName,
        occupation=user.occupation,
        age=user.age,
        city=user.city
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
