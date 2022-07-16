from pydantic import BaseModel, Field


class MovieSchema(BaseModel):
    title: str = Field(...)
    release: int = Field(...)
    gendre: str = Field(...)
    stock: int
    status: str

    class Config:
        schema_extra = {
            "example": {
                "title": "Batman",
                "release": 2015,
                "gendre": "Action",
                "stock": 2,
                "status": 'on-air'
            }
        }


class RateSchema(BaseModel):
    rating: int = Field(...)
    review: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "rating": 4,
                "review": "good quality!",
            }
        }
