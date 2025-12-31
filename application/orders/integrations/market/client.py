import requests


from application.config import settings
from application.orders.shemas.business_order import GetBusinessOrdersResponseDTO
from application.orders.shemas.repo_order import CreateOrderDTO


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

    # print(parsed.orders[0].prices)
    # print(parsed.orders[0].items[0].prices)
    # print(parsed.orders[0].status)
    order_data = parsed.orders[0]

    return order_data


