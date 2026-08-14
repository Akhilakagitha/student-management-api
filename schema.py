from pydantic import BaseModel, ConfigDict


class StudentCreate(BaseModel):
    name: str
    age: int
    email: str
    course: str


class StudentResponse(BaseModel):
    id: int
    name: str
    age: int
    email: str
    course: str

    model_config = ConfigDict(from_attributes=True)