from pydantic import EmailStr, BaseModel, ConfigDict, Field, field_validator
from pydantic.alias_generators import to_camel
import re
from app.models.user import Role

class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra='forbid'
    )

class UserCreate(BaseSchema):
    email: EmailStr
    full_name: str = Field(min_length=3)
    role: Role = Role.FREELANCER
    password: str = Field(min_length=8)

    @field_validator("full_name")
    @classmethod
    def check_name(cls, name: str):
        if not name.replace(" ", "").isalpha():
            raise ValueError("Ismda faqat xarflar kiritilishi shart")
        return name

    @field_validator("password")
    @classmethod
    def password_check(cls, value):
        if not re.search(r"[A-Z]", value) and not re.search(r"[a-z]", value):
            raise ValueError("Parolda kamida bitta katta xarf (A-Z) yoki kamida bitta kichik xarf (a-z) bo'lishi shart")
        if not re.search(r"\d", value) and not re.search(r"[!@#$%^&*_]", value):
            raise ValueError("Parolda kamida bitta raqam (0-9) yoki kamida bitta maxsus belgi (!, @, #, $, %, ^, &, *, _) bo'lishi shart")
        return value

class UserResponse(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="ignore"
    )
    id: int = Field(gt=0)
    role: Role = Role.FREELANCER
    full_name: str = Field(min_length=3)
    email: EmailStr
    is_active: bool = True

class SignUpResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user: UserResponse


