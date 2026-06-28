from fastapi import APIRouter, HTTPException, Depends
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_401_UNAUTHORIZED
from app.repositories import UserRepository, RefreshTokenRepository
from app.core.database import get_async_session
from app.core.security import Hasher, create_access_token, get_current_user,create_refresh_token, ALGORITHM, REFRESH_TOKEN_EXPIRE_DAYS
from app.schemas import UserCreate, SignUpResponse
from app.models import RefreshToken
from datetime import datetime, timezone, timedelta
from app.models import User
import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

router = APIRouter()


@router.post("/login", status_code=200)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_async_session)
):
    user_repo = UserRepository(db)
    refresh_repo = RefreshTokenRepository(db)

    user = await user_repo.get_user_by_email(form_data.username)

    if not user or not Hasher.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Email yoki parol noto'g'ri"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED
        )
    await refresh_repo.clean_up_old_sessions(user.id, 5)


    new_access_token = create_access_token(data={"sub": str(user.id), "email": user.email,"role":user.role})
    new_refresh_token_str, jti = create_refresh_token(data={"sub": str(user.id)})

    hashed_refresh_token_str = Hasher.get_token_hash(new_refresh_token_str)
    new_refresh_token = RefreshToken(
        user_id=user.id,
        token_hash=hashed_refresh_token_str,
        jti=jti,
        expires_at=datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )
    await refresh_repo.create_token(new_refresh_token)

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token_str,
        "token_type": "Bearer",
    }


@router.post("/signup", response_model=SignUpResponse, status_code=201)
async def sign_up(
        user_in: UserCreate,
        db: AsyncSession = Depends(get_async_session)
):
    user_data = user_in.model_dump()

    hashed_pwd = Hasher.get_password_hash(user_in.password)
    user_data["hashed_password"] = hashed_pwd
    del user_data["password"]

    user_repo = UserRepository(db)
    refresh_repo = RefreshTokenRepository(db)

    check_email = await user_repo.get_user_by_email(user_data['email'])
    if check_email:
        raise HTTPException(
            status_code=400,
            detail="Bu email avval ro'yxatdan o'tgan"
        )

    new_user = await user_repo.create_user(user_data)

    access_token = create_access_token(data={"sub": str(new_user.id), "email": new_user.email,"role": new_user.role})
    new_refresh_token_str, jti = create_refresh_token(data={"sub": str(new_user.id)})

    hashed_refresh_token_str = Hasher.get_token_hash(new_refresh_token_str)

    new_db_token = RefreshToken(
        user_id=new_user.id,
        token_hash=hashed_refresh_token_str,
        jti=jti,
        expires_at=datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )
    await refresh_repo.create_token(new_db_token)

    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token_str,
        "token_type": "Bearer",
        "user": new_user,
    }


@router.post("/refresh", status_code=201)
async def refresh_token(
        refresh_token: str,
        db: AsyncSession = Depends(get_async_session)
):
    user_repo = UserRepository(db)
    refresh_repo = RefreshTokenRepository(db)

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, ALGORITHM)
        user_id: str = payload.get("sub")
        type: str = payload.get("type")
        jti: str = payload.get("jti")
        if type is None or type != "refresh" or user_id is None:
            raise HTTPException(
                status_code=401,
                detail="token buzilgan yoki yaroqsiz"
            )
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="token muddati tugagan yoki xato"
        )

    try:
        user = await user_repo.get_user_by_id(int(user_id))
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Foydalanuvchi topilmadi yoki bloklangan"
        )

    if not user or not user.is_active:
        raise HTTPException(
            status_code=401,
            detail="Foydalanuvchi topilmadi yoki bloklangan"
        )

    db_refresh = await refresh_repo.get_token_by_jti(jti)
    if not db_refresh:
        await refresh_repo.delete_all_user_tokens(int(user_id))
        raise HTTPException(status_code=401, detail="Xavfsizlik buzilishi aniqlandi! Qayta login qiling.")

    if not Hasher.verify_password(refresh_token, db_refresh.token_hash):
        raise HTTPException(
            status_code=401,
            detail="Token eskirgan yoki yaroqsiz"
        )

    await refresh_repo.delete_token(db_refresh.id)

    new_access_token = create_access_token(data={"sub": str(user.id), "email": user.email,"role":user.role})
    new_refresh_token_str, jti = create_refresh_token(data={"sub": str(user.id)})

    hashed_refresh_token_str = Hasher.get_token_hash(new_refresh_token_str)

    new_db_token = RefreshToken(
        user_id=user.id,
        token_hash=hashed_refresh_token_str,
        jti=jti,
        expires_at=datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )
    await refresh_repo.create_token(new_db_token)

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token_str,
        "token_type": "Bearer",
    }


@router.get("/me")
async def get_me(
        current_user: User = Depends(get_current_user)
):
    return current_user