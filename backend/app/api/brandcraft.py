import json
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.deps import get_current_user
from app.core.db import get_db
from app.models.entities import User, Project, SearchResult
from app.schemas.dto import ProjectCreate, Step2Territory, Step3Classes, SearchQuery
from app.services.assistant import suggest_classes
from app.services.integrations import parallel_search
from app.services.scoring import compute_score
from app.services.pdf import render_report

router = APIRouter()


@router.post('/step1')
async def step1(payload: ProjectCreate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    project = Project(user_id=user.id, brand_name=payload.brand_name, activity_description=payload.activity_description)
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return {'project_id': project.id, 'status': 'step1_done'}


@router.post('/step1/logo/{project_id}')
async def upload_logo(project_id: int, logo: UploadFile = File(...), user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    project = (await db.execute(select(Project).where(Project.id == project_id, Project.user_id == user.id))).scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail='Project not found')
    content = await logo.read()
    path = f'/tmp/{project_id}_{logo.filename}'
    with open(path, 'wb') as f:
        f.write(content)
    project.logo_path = path
    await db.commit()
    return {'status': 'logo_uploaded'}


@router.post('/step2/{project_id}')
async def step2(project_id: int, payload: Step2Territory, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    project = (await db.execute(select(Project).where(Project.id == project_id, Project.user_id == user.id))).scalar_one_or_none()
    project.territory = payload.territory
    await db.commit()
    return {'status': 'step2_done'}


@router.get('/step3/suggest/{project_id}')
async def step3_suggest(project_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    project = (await db.execute(select(Project).where(Project.id == project_id, Project.user_id == user.id))).scalar_one_or_none()
    return {'suggested': suggest_classes(project.activity_description)}


@router.post('/step3/{project_id}')
async def step3(project_id: int, payload: Step3Classes, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    project = (await db.execute(select(Project).where(Project.id == project_id, Project.user_id == user.id))).scalar_one_or_none()
    project.nice_classes = json.dumps(payload.nice_classes)
    await db.commit()
    return {'status': 'step3_done'}


@router.post('/step4/search')
async def step4(payload: SearchQuery, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    project = (await db.execute(select(Project).where(Project.id == payload.project_id, Project.user_id == user.id))).scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail='Project not found')

    matches = await parallel_search(project.brand_name)
    for m in matches:
        s = compute_score(project.brand_name, m['name'], 0.8, 1.0 if project.territory in ['FRANCE', 'EU', 'INTERNATIONAL'] else 0.3)
        db.add(SearchResult(project_id=project.id, candidate_name=m['name'], source=m.get('source', 'UNKNOWN'), score=s['score'], risk_level=s['risk_level']))
    project.status = 'searched'
    await db.commit()
    return {'status': 'step4_done', 'count': len(matches)}


@router.get('/step5/results/{project_id}')
async def step5(project_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    project = (await db.execute(select(Project).where(Project.id == project_id, Project.user_id == user.id))).scalar_one_or_none()
    res = (await db.execute(select(SearchResult).where(SearchResult.project_id == project.id))).scalars().all()
    return {'results': [{'candidate_name': r.candidate_name, 'source': r.source, 'score': r.score, 'risk_level': r.risk_level} for r in res]}


@router.get('/step6/report/{project_id}')
async def step6(project_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    project = (await db.execute(select(Project).where(Project.id == project_id, Project.user_id == user.id))).scalar_one_or_none()
    res = (await db.execute(select(SearchResult).where(SearchResult.project_id == project.id))).scalars().all()
    rows = [{'candidate_name': r.candidate_name, 'source': r.source, 'score': r.score, 'risk_level': r.risk_level} for r in res]
    pdf = render_report(project.brand_name, rows)
    return Response(content=pdf, media_type='application/pdf')
