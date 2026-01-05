from datetime import datetime
from typing import List, Literal

from pydantic import BaseModel

from application.orders.shemas.enums import *


class NotificationApiErrorDTO(BaseModel):
    message: str
    type: NotificationApiErrorType
    status_code: int


class NotificationReturnItemDTO(BaseModel):
    count: int
    offerId: str


class NotificationUpdatedReturnStatusesDTO(BaseModel):
    refundStatus: RefundStatusType
    shipmentStatus: ReturnShipmentStatusType


class NotificationOrderItemDTO(BaseModel):
    count: int
    offerId: str


class PingNotificationDTO(BaseModel):
    notificationType: NotificationType.PING
    time: datetime

class OrderCreatedNotificationDTO(BaseModel):
    notificationType: Literal[NotificationType.ORDER_CREATED]
    campaignId: int
    createdAt: datetime
    items: List[NotificationOrderItemDTO]
    orderId: int


class OrderStatusUpdatedNotificationDTO(BaseModel):
    notificationType: Literal[NotificationType.ORDER_STATUS_UPDATED]
    campaignId: int
    orderId: int
    status: str
    substatus: str
    updatedAt: datetime


class OrderCancelledNotificationDTO(BaseModel):
    notificationType: NotificationType.ORDER_CANCELLED
    campaignId: int
    cancelledAt: datetime
    items: List[NotificationOrderItemDTO]
    orderId: int


class OrderCancellationRequestNotificationDTO(BaseModel):
    notification_type: NotificationType.ORDER_CANCELLATION_REQUEST
    campaign_id: int
    orderId: int
    requestedAt: datetime


class OrderReturnCreatedNotificationDTO(BaseModel):
    notification_type: NotificationType.ORDER_RETURN_CREATED
    campaignId: int
    createdAt: datetime
    items: List[NotificationOrderItemDTO]
    orderId: int
    returnId: int
    returnType: ReturnType


class OrderReturnStatusUpdatedNotificationDTO(BaseModel):
    notification_type: NotificationType.ORDER_RETURN_STATUS_UPDATED
    campaignId: int
    orderId: int
    returnId: int
    statuses: NotificationUpdatedReturnStatusesDTO
    updatedAt: datetime


class OrderUpdatedNotificationDTO(BaseModel):
    notificationType: Literal[NotificationType.ORDER_UPDATED]
    campaignId: int
    updateType: OrderUpdateType
    updatedAt: datetime

class BaseDTO(BaseModel):
    notificationType: NotificationType