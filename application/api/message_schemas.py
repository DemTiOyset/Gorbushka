from datetime import datetime
from http.client import responses
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from enums import *
from param_shemas import *

from application.api.param_shemas import NotificationOrderItemDTO


class BaseDTO(BaseModel):
    notificationType: NotificationType

class MoneyDTO(BaseModel):
    model_config = ConfigDict(extra="ignore")
    value: float
    currencyId: str

class DeliveryPricesDTO(BaseModel):
    model_config = ConfigDict(extra="ignore")
    payment: Optional[MoneyDTO] = None
    subsidy: Optional[MoneyDTO] = None
    vat: Optional[str] = None

class OrderPricesDTO(BaseModel):
    model_config = ConfigDict(extra="ignore")
    payment: Optional[MoneyDTO] = None
    subsidy: Optional[MoneyDTO] = None
    cashback: Optional[MoneyDTO] = None
    delivery: Optional[DeliveryPricesDTO] = None


class ItemPricesDTO(BaseModel):
    model_config = ConfigDict(extra="ignore")
    payment: Optional[MoneyDTO] = None
    subsidy: Optional[MoneyDTO] = None
    cashback: Optional[MoneyDTO] = None
    vat: Optional[str] = None

class BusinessOrderItemDTO(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: int
    offerId: str
    offerName: str
    count: int
    prices: Optional[ItemPricesDTO] = None

class BusinessOrderShipmentDTO(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: int
    shipmentDate: str
    shipmentTime: Optional[str] = None

class DeliveryOrderDatesDTO(BaseModel):
    model_config = ConfigDict(extra="ignore")
    shipment: Optional[BusinessOrderShipmentDTO] = None

class BusinessOrderDTO(BaseModel):
    model_config = ConfigDict(extra="ignore")
    orderId: int
    campaignId: int
    status: str
    substatus: Optional[str] = None
    items: List[BusinessOrderItemDTO]
    prices: Optional[OrderPricesDTO] = None
    delivery: Optional[DeliveryOrderDatesDTO] = None

class GetBusinessOrdersResponseDTO(BaseModel):
    model_config = ConfigDict(extra="ignore")
    orders: List[BusinessOrderDTO]
    paging: dict = {}

import requests


from application.config import settings

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

    # print(parsed.orders[0].delivery.shipment)
    print(parsed.orders[0].prices)
    print(parsed.orders[0].items[0].prices)
    # print(parsed.orders[0].items[0].offerName)
    # print(parsed.orders[0].items[0].prices.payment.value)

if __name__ == "__main__":
    data = get_order(url=f"https://api.partner.market.yandex.ru/v1/businesses/{settings.business_id}/orders")
    print(data)

# class PingNotificationDTO(BaseModel):
#     notificationType: NotificationType.PING
#     time: datetime
#
#
# class OrderCreatedNotificationDTO(BaseModel):
#     notificationType: Literal[NotificationType.ORDER_CREATED]
#     campaignId: int
#     createdAt: List[datetime]
#     items: List[NotificationOrderItemDTO]
#     orderId: int
#
#
# class OrderStatusUpdatedNotificationDTO(BaseModel):
#     notificationType: NotificationType.ORDER_STATUS_UPDATED
#     campaignId: int
#     orderId: int
#     status: OrderStatusType
#     substatus: OrderSubstatusType
#     updatedAt: datetime
#
#
# class OrderCancelledNotificationDTO(BaseModel):
#     notificationType: NotificationType.ORDER_CANCELLED
#     campaignId: int
#     cancelledAt: datetime
#     items: List[NotificationOrderItemDTO]
#     orderId: int
#
#
# class OrderCancellationRequestNotificationDTO(BaseModel):
#     notification_type: NotificationType.ORDER_CANCELLATION_REQUEST
#     campaign_id: int
#     orderId: int
#     requestedAt: datetime
#
#
# class OrderReturnCreatedNotificationDTO(BaseModel):
#     notification_type: NotificationType.ORDER_RETURN_CREATED
#     campaignId: int
#     createdAt: datetime
#     items: List[NotificationOrderItemDTO]
#     orderId: int
#     returnId: int
#     returnType: ReturnType
#
#
# class OrderReturnStatusUpdatedNotificationDTO(BaseModel):
#     notification_type: NotificationType.ORDER_RETURN_STATUS_UPDATED
#     campaignId: int
#     orderId: int
#     returnId: int
#     statuses: NotificationUpdatedReturnStatusesDTO
#     updatedAt: datetime
#
#
# class OrderUpdatedNotificationDTO(BaseModel):
#     notification_type: NotificationType.ORDER_UPDATED
#     campaignId: int
#     updateType: OrderUpdateType
#     updatedAt: datetime
#
#
#
#

# class GoodsFeedbackCreatedNotificationDTO(BaseModel):
#     notificationType: NotificationType.GOODS_FEEDBACK_CREATED
#     businessId: int
#     createdAt: datetime
#     feedbackId: int
#     publishedAt: datetime
#
#
# class GoodsFeedbackCommentCreatedNotificationDTO(BaseModel):
#     notificationType: NotificationType.GOODS_FEEDBACK_COMMENT_CREATED
#     businessId: int
#     commentId: int
#     createdAt: datetime
#
#
# class ChatCreatedNotificationDTO(BaseModel):
#     notificationType: NotificationType.CHAT_CREATED
#     businessId: int
#     chatId: int
#     createdAt: datetime
#
#
# class ChatMessageSentNotificationDTO(BaseModel):
#     notificationType: NotificationType.CHAT_MESSAGE_SENT
#     businessId: int
#     chatId: int
#     messageId: int
#     sentAt: datetime
#
#
# class ChatArbitrageStartedNotificationDTO(BaseModel):
#     notificationType: NotificationType.CHAT_ARBITRAGE_STARTED
#     businessId: int
#     chatId: int
#     startedAt: datetime
#
#
# class ChatArbitrageFinishedNotificationDTO(BaseModel):
#     notificationType: NotificationType.CHAT_ARBITRAGE_FINISHED
#     businessId: int
#     chatId: int
#     finishedAt: datetime



