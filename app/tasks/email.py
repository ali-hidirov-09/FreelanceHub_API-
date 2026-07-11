import time
from app.schemas import JobCreate
from celery import Celery
import os
from dotenv import load_dotenv
load_dotenv()

celery_app = Celery(
    "freelance_hub",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("REDIS_URL"),
)

@celery_app.task(name="tasks.send_email")
def send_email(job_data: dict):
    job_title = job_data["title"]
    print(f"[Celery] manziliga yangi ish xaqida bilfirishnomani yuborishni boshladi")
    time.sleep(5)
    print(f"[Celery] {job_title} xaqida bildirishnoma freelancerlarga muvaffaqiyatli yuborildi")
    return f"Notification sent to freelancers"