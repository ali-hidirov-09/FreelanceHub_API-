from pydantic import EmailStr, BaseModel, ConfigDict, Field, field_validator
from pydantic.alias_generators import to_camel
from app.models import Role
import re
from datetime import datetime


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra='forbid'
    )

class UserCreate(BaseSchema):
    email: EmailStr
    password: str = Field(min_length=8)
    role: Role = Role.FREELANCER

    @field_validator("password")
    @classmethod
    def password_check(cls, value):
        if not re.search(r"[A-Z]", value):
            raise ValueError("Parolda kamida bitta katta xarf (A-Z) bo'lishi shart")
        if not re.search(r"[a-z]", value):
            raise ValueError("Parolda kamida bitta kichik xarf (a-z) bo'lishi shart")
        if not re.search(r"\d", value):
            raise ValueError("Parolda kamida bitta raqam (0-9) bo'lishi shart")
        if not re.search(r"[!@#$%^&*_]", value):
            raise ValueError("Parolda kamida bitta maxsus belgi (!, @, #, $, %, ^, &, *, _) bo'lishi shart")
        return value


class UserResponse(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="ignore"
    )
    id: int = Field(gt=0)
    email: EmailStr
    role: Role = Role.FREELANCER
    created_at: datetime = datetime.now()
    is_active: bool = True

class SignUpResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse
