from fastapi import APIRouter, HTTPException, status
from fastapi.params import Query
from starlette.status import HTTP_204_NO_CONTENT

from .exceptions import ObjectNotFound
from pydantic import BaseModel, field_validator, ConfigDict, Field,model_validator, SecretStr
from pydantic.alias_generators import to_camel
from typing import Annotated
from app.schemas import JobResponse, JobCreate



router = APIRouter()

class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra='forbid'
    )

PositiveInt = Annotated[int, Field(gt=0)]
PositiveFloat = Annotated[float, Field(gt=0)]
MinStr = Annotated[str, Field(min_length=5, max_length=20)]



#--------------------------------------------------------DAY_7--------------------------------------------------------------------
jobs = [
    {"id": 1, "title": "Python Developer", "min_salary": 1000},
    {"id": 2, "title": "JS Developer", "min_salary": 1500}

]


@router.get("/job/{job_id}")
async def get_job_id(job_id: PositiveInt):
    for i in jobs:
        if i["id"] == job_id:
            return i
    else:
        raise ObjectNotFound(model_name="jobs",obj_id=job_id, status_code=404)


@router.delete("/job/{job_id}", status_code=HTTP_204_NO_CONTENT)
async def delete_job(job_id:PositiveInt):
    for index, job in enumerate(jobs):
        if job["id"] == job_id:
            jobs.pop(index)
            return

    raise ObjectNotFound(model_name="jobs", obj_id=job_id, status_code=410)

#--------------------------------------------------------DAY_5--------------------------------------------------------------------

job_list = []


@router.post("/create", response_model=JobResponse, status_code=201)
async def job_create_2(job: JobCreate):
    job_data = job.model_dump()
    job_data["id"] = len(job_list) + 1
    job_data["status"] = "Active"
    job_data["secret"] = "******"
    job_list.append(job_data)
    print(job_list)
    return job_data


#--------------------------------------------------------DAY_4--------------------------------------------------------------------
#--------------------------------------------------------Vazifa--------------------------------------------------------------------
class UserSchema(BaseSchema):
    username: MinStr
    is_active: bool = True
    email: str
    password: SecretStr

    @field_validator('email')
    @classmethod
    def validate_email_format(cls, v:str):
        if v.count("@") != 1:
            raise ValueError("Email xato formatda kiritildi")
        return v


class JobSchema(BaseSchema):
    title: str = Field(..., min_length=10)
    salary_min: PositiveFloat
    salary_max: PositiveFloat


    @model_validator(mode='after')
    def validate_salary_range(self):
        if self.salary_min > self.salary_max:
            raise ValueError("salary_min salary_max dan katta bo'lishi mumkin emas!")
        return self


@router.post('/job')
async def job_create_1(job:JobSchema):
    jod_data = job.model_dump()
    return {
        "message": "Muvaffaqiyatli yaratildi",
        "data": jod_data
    }


@router.post('/user')
async def user_create_1(user:UserSchema):
    user_data = user.model_dump()
    return {
        "message": "Muvaffaqiyatli yaratildi",
        "data": user_data
    }






#--------------------------------------------------------Dars 4--------------------------------------------------------------------

# devs = [
#     {
#         "id": 1,
#         "category":"IT",
#         "title": "Python",
#         "full_name":"Ali Khidirov",
#         "experience": 1,
#         "salary": 600.0,
#         "description": "Men junior python developerman va kompaniya rivoji uchun hamma narsa qilishga tayyorman."
#     }
# ]
#
# class Job(BaseSchema):
#     category: MinStr
#     title: MinStr
#     is_active: bool = True
#     full_name: MinStr
#     experience: int = Field(..., ge=0)
#     salary: float = Field(..., ge=0.0)
#     description: str
#     created_at: MinStr
#     updated_at: MinStr
#
#     @field_validator('title')
#     @classmethod
#     def is_title_has_python(cls, tit:str):
#         if "python" not in tit.lower():
#             raise  ValueError("Biz faqat Pythonchilarni yaxshi ko'ramiz!")
#         return tit.title()
#
#
#     @field_validator('full_name')
#     @classmethod
#     def full_name_must_be_alpha(cls, s:str):
#         title = s.replace(" ", "")
#         if not title.isalpha():
#             raise ValueError("Ism faqat xarflardan iborat bo'lishi kerak")
#         return s.title()
#
#     @field_validator('salary')
#     @classmethod
#     def salary_must_be_juft(cls, salar:float):
#         sala = int(salar)
#         if sala % 2 != 0:
#             raise ValueError("Faqat juft son kiritish mumkin")
#         return salar
#
#
#     @model_validator(mode='after')
#     def if_is_active_False(self):
#         if self.is_active is False and self.description == "":
#             raise ValueError("Description yozilishi shart")
#         return self
#
#
#
#
#
#
# @router.post('/dev_create')
# async def dev_create(job: Job):
#     global devs
#     job_data = job.model_dump()
#     devs.append(job_data)
#     print(devs)
#     return {"message": "Muvaffaqiyatli yaratildi",
#             "data": job_data}







#--------------------------------------------------------DAY_3--------------------------------------------------------------------
#--------------------------------------------------------DARS + vazifa--------------------------------------------------------------------

# jobs = [
#     {
#         "id": 1,
#         "category":"IT",
#         "name":"Backend",
#         "experience": 2,
#         "about": "Bizga 2 yillik tajribaga ega middle python backend developer kerak. "
#                  "bilishi kk bo'lgan texnologiyalari:Django, DRF, Fast API, Python, Postgresql, Aiogram"
#      },
#     {
#         "id": 2,
#         "category":"IT",
#         "name":"Frontend",
#         "experience": 10,
#         "about": "Bizga 10 yillik tajribaga ega teamlead frontend developer kerak. "
#                  "bilishi kk bo'lgan texnologiyalari:React Native, Next.js, vue.js, Java script, type script, Tailwind"
#      },
#     {
#         "id": 3,
#         "category":"Biznes",
#         "name":"Leader",
#         "experience": 5,
#         "about": "Bizga 5 yillik tajribaga ega katta bizneslarni boshqara poladigan leader kerak. "
#                  "U odam Biznes haqida hamma narsani bilishi kerak"
#      },
#     {
#         "id": 4,
#         "category":"AI",
#         "name":"ML engineer",
#         "experience": 1,
#         "about": "Bizga 1 yillik tajribaga ega strong junior ML engoineer kk. "
#                  "bilishi kk bo'lgan texnologiyalari:ML, Ai bilan ishlash, API, Deep laerning"
#      },
#     {
#         "id": 5,
#         "category":"Biznes",
#         "name":"Salesman",
#         "experience": 20,
#         "about": "Bizga 20 yillik tajribaga ega sotuvchi kerak. "
#                  "bilishi kerak: odamlar bilan muloqot va kassa da professional ishlash mahorati"
#
#      }
# ]


# @router.get("/search/")
# async def get_jobs(
#         keyword: str = Query(..., min_length=3),
#         category: str = Query(None, alias="job-category"),
#         experience: int = Query(None, gt=0, lt=50)
# ):
#     global jobs
#     keyword = keyword.lower()
#     list = []
#     try:
#         for i in jobs:
#             if keyword in i['about'].lower() and (category is None or i['category'] == category) and (
#                     experience is None or i['experience'] == experience):
#                 list.append(i)
#     except Exception as e:
#         return {"xatolik": e}
#     return list