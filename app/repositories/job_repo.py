from typing import Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Job
from app.schemas import JobCreate

class JobRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_jobs(self) -> list[Job]:
        query = select(Job)
        results = await self.session.execute(query)
        return list(results.scalars().all())


    async def get_job_by_id(self, job_id: int) -> Optional[Job]:
        query = select(Job).where(Job.id == job_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()


    async def create_job(self, schema: JobCreate, owner_id:int) -> Job:
        new_job_data = schema.model_dump()
        new_job_data["posted_by_id"] = owner_id
        job_info =Job(**new_job_data)
        self.session.add(job_info)
        await self.session.commit()
        await self.session.refresh(job_info)
        return job_info


    async def update_job(self, job_id: int, update_data: dict[str, Any]) -> Optional[Job]:
        db_job = await self.get_job_by_id(job_id)
        if db_job is None:
            return None

        for k,v in update_data.items():
            if hasattr(db_job, k):
                setattr(db_job, k, v)


        await self.session.commit()
        await self.session.refresh(db_job)
        return db_job


    async def delete_job(self, job_id:int) -> bool:
        job_data = await self.get_job_by_id(job_id)
        if job_data is None:
            return False

        await self.session.delete(job_data)
        await self.session.commit()
        return True



