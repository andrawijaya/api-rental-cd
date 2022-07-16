from pydantic import BaseModel, Field


class RentSchema(BaseModel):
    order_status: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                'order_status': 'process',

            }
        }
