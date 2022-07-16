from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    username: str = Field(...)
    password: str = Field(...)
    gender: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "username": "andra",
                "password": "1234",
                "gender": "Male"
            }
        }
