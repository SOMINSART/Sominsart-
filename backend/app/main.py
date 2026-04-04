from fastapi import FastAPI
from app.api import auth, brandcraft, assistant, dashboard, payment
from app.core.db import Base, engine

app = FastAPI(title='DEPOZIO API')


@app.on_event('startup')
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(auth.router, prefix='/auth', tags=['auth'])
app.include_router(brandcraft.router, prefix='/brandcraft', tags=['brandcraft'])
app.include_router(assistant.router, prefix='/assistant', tags=['assistant'])
app.include_router(dashboard.router, prefix='/dashboard', tags=['dashboard'])
app.include_router(payment.router, prefix='/payments', tags=['payments'])


@app.get('/health')
async def health():
    return {'status': 'ok'}
