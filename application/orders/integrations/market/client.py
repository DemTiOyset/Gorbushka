import asyncio

import requests


from application.config import settings
from application.orders.shemas.notifications import GetBusinessOrdersResponseDTO


from application.orders.test_json import a as test_json


async def get_order(
        campaign_id: int,
        order_id: int,
        url: str = f"https://"
                   f"api.partner.market.yandex.ru/v1/businesses/"
                   f"{settings.business_id}/orders",
):
    params = {
        "campaignIds": [campaign_id],
        "orderIds": [order_id]
        }

    headers = {
         "Api-Key": settings.api_key,
        "Content-Type": "application/json",
    }

    response = requests.post(url, headers=headers, json=params)
    response.raise_for_status()

    payload = response.json()
    parsed = GetBusinessOrdersResponseDTO.model_validate(payload)

    order_data = parsed.orders[0]

    return order_data

