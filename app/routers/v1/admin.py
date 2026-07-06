from fastapi import APIRouter
from fastapi.params import Depends
from app.core.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import UserResponse
from app.repositories import UserRepository
from app.core.dependencies import require_role
from app.models import User, Role

router = APIRouter()

@router.get("/users", response_model=list[UserResponse], status_code=200)
async def get_all_users(
        db: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(require_role([Role.ADMIN]))
):
    repo = UserRepository(db)
    users = await repo.get_all_users()
    return users


