import asyncio
import httpx
from app.core.config import settings


async def _fetch(endpoint: str, brand_name: str):
    try:
        async with httpx.AsyncClient(timeout=4) as client:
            r = await client.get(endpoint, params={'q': brand_name})
            if r.status_code == 200:
                data = r.json()
                if isinstance(data, list):
                    return data
    except Exception:
        pass
    return [
        {'name': f'{brand_name} Prime', 'source': endpoint.split('//')[1].split('.')[1].upper()},
        {'name': f'{brand_name} Pro', 'source': endpoint.split('//')[1].split('.')[1].upper()},
    ]


async def parallel_search(brand_name: str):
    results = await asyncio.gather(
        _fetch(settings.inpi_endpoint, brand_name),
        _fetch(settings.euipo_endpoint, brand_name),
        _fetch(settings.wipo_endpoint, brand_name),
    )
    flat = []
    for group in results:
        flat.extend(group)
    return flat
