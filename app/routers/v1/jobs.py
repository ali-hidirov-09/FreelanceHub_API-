from fastapi import APIRouter
from fastapi.params import Query

router = APIRouter()


jobs = [
    {
        "id": 1,
        "category":"IT",
        "name":"Backend",
        "experience": 2,
        "about": "Bizga 2 yillik tajribaga ega middle python backend developer kerak. "
                 "bilishi kk bo'lgan texnologiyalari:Django, DRF, Fast API, Python, Postgresql, Aiogram"
     },
    {
        "id": 2,
        "category":"IT",
        "name":"Frontend",
        "experience": 10,
        "about": "Bizga 10 yillik tajribaga ega teamlead frontend developer kerak. "
                 "bilishi kk bo'lgan texnologiyalari:React Native, Next.js, vue.js, Java script, type script, Tailwind"
     },
    {
        "id": 3,
        "category":"Biznes",
        "name":"Leader",
        "experience": 5,
        "about": "Bizga 5 yillik tajribaga ega katta bizneslarni boshqara poladigan leader kerak. "
                 "U odam Biznes haqida hamma narsani bilishi kerak"
     },
    {
        "id": 4,
        "category":"AI",
        "name":"ML engineer",
        "experience": 1,
        "about": "Bizga 1 yillik tajribaga ega strong junior ML engoineer kk. "
                 "bilishi kk bo'lgan texnologiyalari:ML, Ai bilan ishlash, API, Deep laerning"
     },
    {
        "id": 5,
        "category":"Biznes",
        "name":"Salesman",
        "experience": 20,
        "about": "Bizga 20 yillik tajribaga ega sotuvchi kerak. "
                 "bilishi kerak: odamlar bilan muloqot va kassa da professional ishlash mahorati"

     }
]

@router.get("/search/")
async def get_jobs(
        keyword: str = Query(..., min_length=3),
        category: str = Query(None, alias="job-category"),
        experience:  int = Query(gt=0, lt=50)
):
    global jobs
    keyword.lower()
    try:
        for i in jobs:
            if i['about'].lower().find(keyword) and i['category'] == category and i['experience'] == experience:
                return i
            elif i['about'].lower().find(keyword) and i['experience'] == experience:
                return i
    except Exception as e:
        return {"xatolik": e}

    return {
        "message": "Bunday kasb topilmadi"
    }


