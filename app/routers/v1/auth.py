from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_403_FORBIDDEN, HTTP_401_UNAUTHORIZED

from app.repositories import UserRepository
from app.core.database import get_async_session
from app.core.security import hasher, create_access_token
from app.schemas import UserCreate, SignUpResponse

router = APIRouter()


@router.post("/login", status_code=200)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_async_session)
):
    repo = UserRepository(db)
    user = await repo.get_user_by_email(form_data.username)

    if not user or not hasher.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Email yoki parol noto'g'ri"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED
        )

    token = create_access_token(data={"sub": user.email, "role": user.role})
    return {
        "access_token": token, "token_type": "Bearer"
    }


@router.post("/signup", response_model=SignUpResponse, status_code=201)
async def sign_up(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_async_session)
):

    user_data = user_in.model_dump()

    hashed_pwd = hasher.get_password_hash(user_in.password)
    user_data["hashed_password"] = hashed_pwd
    del user_data["password"]

    repo = UserRepository(db)

    check_email = await repo.get_user_by_email(user_in.email)
    if check_email:
        raise HTTPException(
            status_code=400,
            detail="Bu email avval ro'yxatdan o'tgan"
        )

    new_user = await repo.create_user(user_data)
    token = create_access_token(data={"sub": new_user.email, "role": new_user.role})
    return {
        "access_token": token,
        "token_type": "Bearer",
        "user": new_user,
    }
