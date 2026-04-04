from fastapi import APIRouter, Depends, HTTPException
from google.oauth2 import id_token
from google.auth.transport import requests
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.config import settings
from app.core.db import get_db
from app.models.entities import User, RefreshToken
from app.schemas.dto import RegisterRequest, LoginRequest, TokenResponse
from app.services.auth import hash_password, verify_password, create_access_token, create_refresh_token, get_user_by_email, store_refresh_token

router = APIRouter()


@router.post('/register', response_model=TokenResponse)
async def register(payload: RegisterRequest, db: AsyncSession = Depends(get_db)):
    if await get_user_by_email(db, payload.email):
        raise HTTPException(status_code=409, detail='Email already exists')
    user = User(email=payload.email, password_hash=hash_password(payload.password), is_google=False)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    access = create_access_token(str(user.id))
    refresh, exp = create_refresh_token(str(user.id))
    await store_refresh_token(db, user.id, refresh, exp)
    return TokenResponse(access_token=access, refresh_token=refresh)


@router.post('/login', response_model=TokenResponse)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    access = create_access_token(str(user.id))
    refresh, exp = create_refresh_token(str(user.id))
    await store_refresh_token(db, user.id, refresh, exp)
    return TokenResponse(access_token=access, refresh_token=refresh)


@router.post('/refresh', response_model=TokenResponse)
async def refresh(token: str, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(RefreshToken).where(RefreshToken.token == token))
    existing = res.scalar_one_or_none()
    if not existing:
        raise HTTPException(status_code=401, detail='Invalid refresh token')
    access = create_access_token(str(existing.user_id))
    new_refresh, exp = create_refresh_token(str(existing.user_id))
    await store_refresh_token(db, existing.user_id, new_refresh, exp)
    return TokenResponse(access_token=access, refresh_token=new_refresh)


@router.post('/google', response_model=TokenResponse)
async def google_oauth(id_token_str: str, db: AsyncSession = Depends(get_db)):
    try:
        payload = id_token.verify_oauth2_token(id_token_str, requests.Request(), settings.google_client_id)
        email = payload['email']
    except Exception as exc:
        raise HTTPException(status_code=401, detail='Invalid Google token') from exc

    user = await get_user_by_email(db, email)
    if not user:
        user = User(email=email, password_hash=hash_password('google-user'), is_google=True)
        db.add(user)
        await db.commit()
        await db.refresh(user)

    access = create_access_token(str(user.id))
    refresh, exp = create_refresh_token(str(user.id))
    await store_refresh_token(db, user.id, refresh, exp)
    return TokenResponse(access_token=access, refresh_token=refresh)
