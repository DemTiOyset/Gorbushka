import requests


from application.config import settings
from application.orders.shemas.order import GetBusinessOrdersResponseDTO


def get_order(
        url: str,
):
    params = {
        "campaignIds": [settings.campaign_id],
        "orderIds": ["52701397891"]
        }

    headers = {
         "Api-Key": settings.api_key,
        "Content-Type": "application/json",
    }

    response = requests.post(url, headers=headers, json=params)
    response.raise_for_status()

    data = response.json()
    parsed = GetBusinessOrdersResponseDTO.model_validate(data)

    print(parsed.orders[0].prices)
    print(parsed.orders[0].items[0].prices)

if __name__ == "__main__":
    data = get_order(url=f"https://api.partner.market.yandex.ru/v1/businesses/{settings.business_id}/orders")
    print(data)