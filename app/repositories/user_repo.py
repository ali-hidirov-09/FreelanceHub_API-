from typing import Optional, Any

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from app.models import User, Job

class UserRepository:
    def __init__(self,session: AsyncSession):
        self.session = session

    async def create_user(self, user_data) -> User:
        new_user = User(**user_data)
        self.session.add(new_user)
        try:
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise ValueError("Bu email manzili allaqachon ro'yhatdan o'tkazilgan")
        await self.session.refresh(new_user)
        return new_user


    async def get_jobs_by_users(self):
        query = select(User).options(selectinload(User.jobs))
        results = await self.session.execute(query)
        users = results.scalars().all()
        for user in users:
            print(f"User: {user.email}: Job count: {len(user.jobs)}, Jobs: {user.jobs}")
        return list(users)


    async def get_user_by_email(self, email: str) -> Optional[User]:
        query = select(User).filter(User.email == email)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()



