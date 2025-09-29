import asyncio
import random
from typing import Any, Dict, Optional

import httpx


DEFAULT_HEADERS: Dict[str, str] = {
    "User-Agent": "BookScraper/1.0 (+https://example.local)"
}


async def get_json_with_client(
    client: httpx.AsyncClient,
    url: str,
    *,
    params: Optional[Dict[str, Any]] = None,
    retries: int = 3,
    backoff_base: float = 0.5,
) -> Dict[str, Any]:
    attempt = 0
    while True:
        attempt += 1
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception:
            if attempt >= retries:
                raise
            sleep_s = backoff_base * (2 ** (attempt - 1)) + random.uniform(0, 0.2)
            await asyncio.sleep(sleep_s)


async def get_json(
    url: str,
    *,
    params: Optional[Dict[str, Any]] = None,
    timeout: float = 20.0,
    retries: int = 3,
    backoff_base: float = 0.5,
) -> Dict[str, Any]:
    async with httpx.AsyncClient(timeout=timeout, headers=DEFAULT_HEADERS) as client:
        return await get_json_with_client(
            client, url, params=params, retries=retries, backoff_base=backoff_base
        )
