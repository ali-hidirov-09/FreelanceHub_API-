from typing import Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class JobRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    from app.models import Job
    async def get_all(self) -> list[Job]:
        from app.models import Job
        query = select(Job)
        results = await self.session.execute(query)
        return list(results.scalars().all())


    async def get_by_id(self, job_id: int) -> Optional[Job]:
        from app.models import Job
        query = select(Job).where(Job.id == job_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()


    async def create(self, job_data: Job) -> Job:
        self.session.add(job_data)
        await self.session.commit()
        await self.session.refresh(job_data)
        return job_data


    async def update(self, job_id: int, update_data: dict[str, Any]) -> Optional[Job]:
        db_job = await self.get_by_id(job_id)
        if db_job is None:
            return None

        for k,v in update_data.items():
            if hasattr(db_job, k):
                setattr(db_job, k, v)


        await self.session.commit()
        await self.session.refresh(db_job)
        return db_job


    async def delete(self, job_id:int) -> bool:
        job_data = await self.get_by_id(job_id)
        if job_data is None:
            return False

        await self.session.delete(job_data)
        await self.session.commit()
        return True



