from typing import Iterable

from pydantic import BaseModel

from application.orders.shemas.enums import OrderUpdateType
from application.orders.shemas.message import OrderStatusUpdatedNotificationDTO, OrderCreatedNotificationDTO, \
    OrderCancelledNotificationDTO, OrderReturnCreatedNotificationDTO, OrderUpdatedNotificationDTO
from application.orders.shemas.notifications import BusinessOrderDTO
from application.orders.shemas.orders import OrderDTO, CreateOrderItemsDTO


async def _validate_order_created(notification: OrderCreatedNotificationDTO) -> OrderDTO:
    dto = _to_order_dto(notification, include={"orderId", "campaignId", "createdAt"})
    dto.status = "CREATED"

    return dto


async def _validate_order_items(
        order_data: BusinessOrderDTO,
) -> list[CreateOrderItemsDTO]:

    shipping_date = order_data.delivery.shipment.shipmentDate

    order_items: list[CreateOrderItemsDTO] = []
    for item in order_data.items:

        order_item = CreateOrderItemsDTO.model_validate({
            "quantity": item.count,
            "shipping_date": shipping_date,
            "price_from_market": item.prices.payment.value,
            "product_name": item.offerName,
            "market_costs": item.prices.payment.value,
            "market_commission": item.prices.subsidy.value,
        })
        order_items.append(order_item)

    return order_items

async def _validate_order_update_status(notification: OrderStatusUpdatedNotificationDTO) -> OrderDTO:
    return _to_order_dto(notification, include={"orderId", "campaignId", "updatedAt", "status", "substatus"})


async def _validate_cancelled_order(notification: OrderCancelledNotificationDTO) -> OrderDTO:
    dto = _to_order_dto(notification, include={"orderId", "campaignId", "cancelledAt"})

    dto.status = "CANCELLED"
    return dto

async def _validate_return_order(notification: OrderReturnCreatedNotificationDTO) -> OrderDTO:
    dto = _to_order_dto(notification, include={"orderId", "campaignId", "createdAt"})
    dto.status = "RETURN"

    return dto

async def _validate_updated_order(notification: OrderUpdatedNotificationDTO) -> OrderDTO:
    dto = _to_order_dto(notification, include={"orderId", "campaignId", "updatedAt"})
    update_type = notification.updateType

    if update_type == OrderUpdateType.SHIPMENT_DATE_UPDATED:
        return dto

    return None

def _to_order_dto(notification: BaseModel, include: Iterable[str]) -> OrderDTO:
    return OrderDTO.model_validate(
        notification.model_dump(
            include=set(include),
            exclude_unset=True,
            by_alias=False,
        )
    )

