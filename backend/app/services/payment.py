import stripe
from app.core.config import settings

stripe.api_key = settings.stripe_secret_key


def create_checkout_session(project_id: int, amount_eur: int):
    vat_amount = int(amount_eur * 0.2)
    total = amount_eur + vat_amount
    return stripe.checkout.Session.create(
        mode='payment',
        success_url=f'{settings.frontend_url}/success?project={project_id}',
        cancel_url=f'{settings.frontend_url}/cancel?project={project_id}',
        line_items=[{
            'price_data': {
                'currency': 'eur',
                'unit_amount': total * 100,
                'product_data': {'name': f'DEPOZIO Filing Assistant #{project_id}'},
            },
            'quantity': 1,
        }],
        metadata={'project_id': str(project_id), 'vat_rate': '20%'}
    )
