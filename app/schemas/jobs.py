from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from typing import Annotated
from pydantic.alias_generators import to_camel


MinStr = Annotated[str, Field(min_length=3)]


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra='forbid'
    )


class JobCreate(BaseSchema):
    title: MinStr
    description: str = Field(..., min_length=10)
    salary: float = Field(..., gt=0)

    @field_validator('title')
    @classmethod
    def validate_title(cls, v:str):
        if not v.isalpha():
            raise ValueError("Faqat xarflar kiritilishi shart")
        return v.title()



class JobResponse(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra='ignore'
    )
    id: int = Field(..., gt=0)
    title: MinStr
    description: str = Field(..., min_length=10)
    salary: float = Field(..., gt=0)
    status: str = "Active"

    @field_validator('title')
    @classmethod
    def validate_title(cls, v: str):
        if not v.isalpha():
            raise ValueError("Faqat xarflar kiritilishi shart")
        return v.title()
