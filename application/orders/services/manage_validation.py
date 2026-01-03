from application.orders.shemas.message import OrderStatusUpdatedNotificationDTO, OrderCreatedNotificationDTO
from application.orders.shemas.notifications import BusinessOrderDTO
from application.orders.shemas.orders import OrderDTO, CreateOrderItemsDTO


async def _validate_order_created(notification: OrderCreatedNotificationDTO) -> OrderDTO:
    order_data: OrderDTO = OrderDTO.model_validate(
        notification.model_dump(
            include={"orderId", "campaignId", "createdAt"},
            exclude_unset=True,
            by_alias=False,
        )
    )
    order_data.status = "CREATED"
    return order_data


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
    order_data: OrderDTO = OrderDTO.model_validate(
        notification.model_dump(
            include={"orderId", "campaignId", "updatedAt", "status", "substatus"},
            exclude_unset=True,
            by_alias=False,
        )
    )
    return order_data