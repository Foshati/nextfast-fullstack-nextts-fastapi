from sqlalchemy import Column, Integer, String
from .database import Base

class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, index=True)
    firstName = Column(String, index=True)
    lastName = Column(String, index=True)
    occupation = Column(String)
    age = Column(Integer)
    city = Column(String)
