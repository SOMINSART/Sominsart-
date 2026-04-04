from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.schemas.dto import PaymentRequest
from app.services.payment import create_checkout_session

router = APIRouter()


@router.post('/checkout')
async def checkout(payload: PaymentRequest, _=Depends(get_current_user)):
    session = create_checkout_session(payload.project_id, payload.amount_eur)
    return {'checkout_url': session.url, 'id': session.id}
