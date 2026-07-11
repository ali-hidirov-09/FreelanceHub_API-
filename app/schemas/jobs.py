from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Annotated
from pydantic.alias_generators import to_camel
from app.models import JobStatus
from datetime import datetime

MinStr = Annotated[str, Field(min_length=3)]
BigStr = Annotated[str, Field(min_length=20)]
PositiveInt = Annotated[int, Field(gt=0)]
PositiveFloat = Annotated[float, Field(gt=0.0)]

class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra='forbid'
    )



class JobCreate1(BaseSchema):
    title: MinStr
    description: BigStr
    category: MinStr
    salary: PositiveFloat
    salary_currency: str = Field(min_length=1, max_length=3)
    status: JobStatus = Field(default=JobStatus.OPEN)
    deadline: datetime = Field(description="E'lonning tugash vaqti")




class JobCreate(BaseSchema):
    category: MinStr
    title: MinStr
    description: str = Field(..., min_length=10)
    salary: float = Field(..., gt=0)
    salary_currency: str = Field(min_length=2, default="USD")
    status: JobStatus = JobStatus.OPEN
    deadline: datetime

    @field_validator('title')
    @classmethod
    def validate_title(cls, v:str):
        if not v.replace(" ", "").isalpha():
            raise ValueError("Faqat xarflar kiritilishi shart")
        return v.title()



class JobResponseData(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra='ignore'
    )
    id: int = Field(..., gt=0)
    category: MinStr
    title: MinStr
    description: str = Field(..., min_length=10)
    salary: float = Field(..., gt=0)
    salary_currency: str = Field(min_length=2, default="USD")
    status: JobStatus = JobStatus.OPEN
    posted_by_id: int = Field(gt=0)
    deadline: datetime

    created_at: datetime

    @field_validator('title')
    @classmethod
    def validate_title(cls, v: str):
        if not v.replace(" ", "").isalpha():
            raise ValueError("Faqat xarflar kiritilishi shart")
        return v.title()


class JobResponse(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra='ignore'
    )
    data: JobResponseData
    message: str