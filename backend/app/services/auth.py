from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.models.entities import User, RefreshToken

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def create_access_token(subject: str) -> str:
    exp = datetime.utcnow() + timedelta(minutes=settings.jwt_exp_minutes)
    return jwt.encode({'sub': subject, 'exp': exp}, settings.jwt_secret, algorithm='HS256')


def create_refresh_token(subject: str) -> tuple[str, datetime]:
    exp = datetime.utcnow() + timedelta(days=settings.jwt_refresh_days)
    token = jwt.encode({'sub': subject, 'exp': exp}, settings.jwt_refresh_secret, algorithm='HS256')
    return token, exp


async def store_refresh_token(db: AsyncSession, user_id: int, token: str, expires_at: datetime):
    db.add(RefreshToken(user_id=user_id, token=token, expires_at=expires_at))
    await db.commit()


async def get_user_by_email(db: AsyncSession, email: str):
    res = await db.execute(select(User).where(User.email == email))
    return res.scalar_one_or_none()


def decode_access(token: str) -> str:
    return jwt.decode(token, settings.jwt_secret, algorithms=['HS256'])['sub']
