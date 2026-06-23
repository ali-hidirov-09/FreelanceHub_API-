from typing import Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from app.models import User, Job

class UserRepository:
    def __init__(self,session):
        self.session = session

    async def create_user(self, user_data: User) -> User:
        self.session.add(user_data)
        await self.session.commit()
        await self.session.refresh(user_data)
        return user_data


    async def get_jobs_by_users(self):
        query = select(User).options(selectinload(User.jobs))
        results = await self.session.execute(query)
        users = results.scalars().all()
        for user in users:
            print(f"User: {user.email}: Job count: {len(user.jobs)}, Jobs: {user.jobs}")
        return list(users)


