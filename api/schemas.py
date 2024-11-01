from pydantic import BaseModel

class UserCreate(BaseModel):
    firstName: str
    lastName: str
    occupation: str
    age: int
    city: str

class UserResponse(BaseModel):
    id: int
    firstName: str
    lastName: str
    occupation: str
    age: int
    city: str

    class Config:
        orm_mode = True
