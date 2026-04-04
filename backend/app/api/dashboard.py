from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.deps import get_current_user
from app.core.db import get_db
from app.models.entities import User, Project

router = APIRouter()


@router.get('/projects')
async def list_projects(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(Project).where(Project.user_id == user.id))).scalars().all()
    return {'projects': [{'id': p.id, 'brand_name': p.brand_name, 'status': p.status, 'territory': p.territory} for p in rows]}
