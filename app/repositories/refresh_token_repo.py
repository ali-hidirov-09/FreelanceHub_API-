from typing import Optional

from sqlalchemy import select, delete
from app.models import RefreshToken


class RefreshTokenRepository:
    def __init__(self, session):
        self.session = session

    async def get_token_by_jti(self, jti: str) -> Optional[str]:
        query = select(RefreshToken).where(RefreshToken.jti == jti)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create_token(self, token_data: RefreshToken):
        self.session.add(token_data)
        await self.session.commit()
        await self.session.refresh(token_data)
        return token_data

    async def clean_up_old_sessions(self, user_id: int, max_sessions: int = 5):
        query = (
            select(RefreshToken).where(RefreshToken.user_id == user_id)
            .order_by(RefreshToken.created_at.desc())
        )
        results = await self.session.execute(query)
        tokens = list(results.scalars().all())

        if len(tokens) >= max_sessions:
            for old_token in tokens[max_sessions - 1:]:
                await self.session.delete(old_token)
            await self.session.commit()

    async def get_token_by_token_id(self, token_id):
        query = select(RefreshToken).where(RefreshToken.id == token_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_token_by_user_id(self, user_id):
        query = select(RefreshToken).where(RefreshToken.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def delete_token(self, token_id):
        token_data = await self.get_token_by_token_id(token_id)
        if token_data is None:
            return False

        await self.session.delete(token_data)
        await self.session.commit()
        return True

    async def delete_all_user_tokens(self, user_id: int):
        query = delete(RefreshToken).where(RefreshToken.user_id == user_id)
        result = await self.session.execute(query)
        await self.session.commit()

        return result.rowcount > 0
