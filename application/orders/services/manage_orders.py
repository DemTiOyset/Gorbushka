import asyncio
from datetime import date

from application.db import async_session_maker
from application.orders.models.order import Order
from application.orders.test_json import a as test_json

from application.orders.integrations.market.client import get_order
from application.orders.repo import OrderRepository
from application.orders.shemas.business_order import BusinessOrderDTO
from application.orders.shemas.repo_order import CreateOrderDTO


async def process_notification_payload(payload: dict) -> dict:
    """Distribution of tasks based on the received notification."""
    data_from_notifications = await _validate_notifications(payload)
    unprocessed_order = await get_order(
        payload["campaign_id"],
        payload["order_id"]
    )
    dtos = await _validate_orders_for_database(unprocessed_order)
    for dto in dtos:
        order = dto_to_order(dto)
        async with async_session_maker() as session:
            async with session.begin():
                await OrderRepository.create(session=session, order=order)

    if payload["notificationType"] == "ORDER_CREATED":
        """Написать логику для создания заказа."""
    elif payload["notificationType"] == "ORDER_UPDATED":
        """
        Написать логику для обновления заказа
        (нужно дополнительно проверить тип обновления).
        """
    elif payload["notificationType"] == "ORDER_CANCELED":
        """
        Написать логику для отмены заказа
        (нужно дополнительно проверить тип отмены).
        """


async def _validate_notifications(notification_payload: dict) -> dict:
    """Потом разберусь."""

async def _validate_orders_for_database(order_data: BusinessOrderDTO) -> list[CreateOrderDTO]:
    base = CreateOrderDTO.model_validate(
        order_data.model_dump(
            include={"orderId", "campaignId", "status"},
            exclude_unset=True,
            by_alias=False,
        )
    )

    quantity = len(order_data.items)
    shipping_date = order_data.delivery.shipment.shipmentDate

    orders: list[CreateOrderDTO] = []
    for item in order_data.items:
        dto = CreateOrderDTO.model_validate({
            **base.model_dump(),
            "quantity": quantity,
            "shipping_date": shipping_date,
            "market_cost": item.prices.payment,
            "product_name": item.offerName,
        })
        orders.append(dto)

    return orders


def dto_to_order(dto: CreateOrderDTO) -> Order:
    return Order(
        campaign_id=dto.campaign_id,
        market_order_id=dto.market_order_id,
        status=dto.status,          # если enum -> строка, ок
        substatus=dto.substatus,
        product_name=dto.product_name,
        quantity=dto.quantity,
        price_from_market=dto.price_from_market,
        market_commission=dto.market_commission,
        market_costs=dto.market_costs,
        discount=dto.discount,
        shipping_date=date.fromisoformat(dto.shipping_date) if dto.shipping_date else None,
    )

asyncio.run(process_notification_payload(test_json))
