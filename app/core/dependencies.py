from .security import ALGORITHM, SECRET_KEY, oauth2_scheme
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import UserRepository
from .database import get_async_session
from app.models import User, Role

async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_async_session)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id: str = payload.get("sub")
        type: str = payload.get("type")
        if type is None or type != "access":
            raise HTTPException(
                status_code=401,
                detail="token buzilgan yoki yaroqsiz"
            )
        if id is None:
            raise HTTPException(
                status_code=401,
                detail="token yaroqsiz"
            )

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="token muddati tugagan yoki xato"
        )
    if not id.isnumeric():
        raise HTTPException(status_code=403, detail="Ma'lumotlaringiz buzilgan")

    repo = UserRepository(db)
    try:
        user = await repo.get_user_by_id(int(id))
    except Exception:
        raise HTTPException(
            status_code=401
        )

    if not user or not user.is_active:
        raise HTTPException(
            status_code=401,
            detail="Foydalanuvchi topilmadi yoki bloklangan"
        )

    return user


def require_role(allowed_roles: list[Role]):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Sizga bu ishni amalga oshirish uchun ruxsat yo'q")
        return current_user
    return role_checker