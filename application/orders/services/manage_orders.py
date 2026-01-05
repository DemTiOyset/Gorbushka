import asyncio
import logging
from datetime import date
from typing import List, Any

from sqlalchemy.exc import IntegrityError

from application.orders.models.orders import Orders
from application.orders.services.manage_repo import update_order_status, create_order_with_items, \
    update_cancelled_order, update_return_status, update_order_shipment_date
from application.orders.services.manage_validation import _validate_order_update_status, _validate_order_items, \
    _validate_order_created, _validate_cancelled_order, _validate_return_order, _validate_updated_order
from application.orders.shemas.enums import NotificationType
from application.orders.shemas.message import OrderCreatedNotificationDTO, OrderStatusUpdatedNotificationDTO, \
    OrderCancelledNotificationDTO, OrderUpdatedNotificationDTO
from application.orders.shemas.notifications import GetBusinessOrdersResponseDTO
from application.orders.test_json import updated as test_json

from application.orders.integrations.market.client import get_order
from application.orders.shemas.orders import OrderDTO, CreateOrderItemsDTO

log = logging.getLogger(__name__)

class ManageOrders:
    """Manage orders."""
    def __init__(self, payload: dict) -> None:
        self.payload = payload

    async def handle_order(self) -> dict[str, Any]:
        handler = HANDLERS.get(self.payload.get("notificationType"))
        if handler is None:

            return {"message": "ignored", "reason": "unsupported_notification_type"}

        return await handler(self)

    async def handle_order_created(self) -> dict[str, Any]:
        unprocessed_order = await get_order(
            self.payload["campaignId"],
            self.payload["orderId"]
        )

        created_notification = OrderCreatedNotificationDTO.model_validate(self.payload)

        order_dto: OrderDTO = await _validate_order_created(created_notification)

        items_dto: list[CreateOrderItemsDTO] = await _validate_order_items(
            order_data=unprocessed_order,
        )

        try:
            order_model: Orders = await create_order_with_items(order_dto, items_dto)
        except IntegrityError:
            log.exception("Integrity error while creating order")

            return {"message": "duplicate_or_integrity_error"}
        except Exception as e:
            log.exception("Unexpected error while creating order")

            return {"message": "error", "detail": str(e)}

        return {"message": "ok", "handled": "ORDER_CREATED", "order_id": order_model.id}

    async def handle_order_updated(self):
        unprocessed_order = await get_order(self.payload["campaignId"], self.payload["orderId"])

        updated_notification = OrderUpdatedNotificationDTO.model_validate(self.payload)

        try:
            if updated_notification is not None:
                order_dto = await update_order_shipment_date(unprocessed_order)

        except IntegrityError:
            log.exception("Integrity error while creating order")

            return {"message": "duplicate_or_integrity_error"}
        except Exception as e:
            log.exception("Unexpected error while creating order")

            return {"message": "error", "detail": str(e)}

        return {"message": "ok", "handled": "ORDER_UPDATED"}

    async def handle_order_updated_status(self) -> dict[str, Any]:
        updated_notification = OrderStatusUpdatedNotificationDTO.model_validate(self.payload)

        order_dto = await _validate_order_update_status(updated_notification)
        try:
            order_model: Orders = await update_order_status(order_dto)
        except IntegrityError as e:
            return {"message": "duplicate_or_integrity_error"}
        except Exception as e:
            return {"message": "error", "detail": str(e)}
        return {"message": "ok", "handled": "ORDER_STATUS_UPDATED"}

    async def handle_order_cancelled(self) -> dict[str, Any]:
        cancelled_notification = OrderCancelledNotificationDTO.model_validate(self.payload)

        order_dto = await _validate_cancelled_order(cancelled_notification)

        try:
            order_model: Orders = await update_cancelled_order(order_dto)
        except IntegrityError as e:
            return {"message": "duplicate_or_integrity_error"}
        except Exception as e:
            return {"message": "error", "detail": str(e)}
        return {"message": "ok", "handled": "ORDER_STATUS_CANCELED"}

    async def handle_order_return(self) -> dict[str, Any]:
        return_notification = OrderCancelledNotificationDTO.model_validate(self.payload)

        order_dto = await _validate_return_order(return_notification)

        try:
            order_model: Orders = await update_return_status(order_dto)
        except IntegrityError as e:

            return {"message": "duplicate_or_integrity_error"}
        except Exception as e:

            return {"message": "error", "detail": str(e)}
        return {"message": "ok", "handled": "ORDER_STATUS_RETURN"}



HANDLERS: dict = {
    NotificationType.ORDER_CREATED: ManageOrders.handle_order_created,
    NotificationType.ORDER_STATUS_UPDATED: ManageOrders.handle_order_updated_status,
}

manage_order = ManageOrders(test_json)

asyncio.run(manage_order.handle_order_updated())

