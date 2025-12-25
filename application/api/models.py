from datetime import datetime
from enums import *
from typing import List

from pydantic import BaseModel


class PingNotificationDTO(BaseModel):
    notificationType: NotificationType.PING
    time: datetime


class NotificationOrderItemDTO(BaseModel):
    count: int
    offerId: str



class OrderCreatedNotificationDTO(BaseModel):
    notificationType: NotificationType.ORDER_CREATED
    campaignId: int
    createdAt: List[datetime]
    items: List[NotificationOrderItemDTO]
    orderId: int


class OrderStatusUpdatedNotificationDTO(BaseModel):
    notificationType: NotificationType.ORDER_STATUS_UPDATED
    campaignId: int
    orderId: int
    status: OrderStatusType
    substatus: OrderSubstatusType
    updatedAt: datetime


class OrderCancelledNotificationDTO(BaseModel):
    notificationType: NotificationType.ORDER_CANCELLED
    campaignId: int
    cancelledAt: datetime
    items: List[NotificationOrderItemDTO]
    orderId: int


class OrderCancellationRequestNotificationDTO:
    notificationType: NotificationType.ORDER_CANCELLATION_REQUEST
    campaignId: int
    orderId: int
    requestedAt: datetime


class OrderReturnCreatedNotificationDTO(BaseModel):
    notificationType: NotificationType.ORDER_RETURN_CREATED
    campaignId: int
    createdAt: datetime
    items: List[NotificationOrderItemDTO]
    orderId: int
    returnId: int
    returnType: ReturnType


class NotificationUpdatedReturnStatusesDTO(BaseModel):
    refundStatus: RefundStatusType
    shipmentStatus: ReturnShipmentStatusType



class OrderReturnStatusUpdatedNotificationDTO(BaseModel):
    notificationType: NotificationType.ORDER_RETURN_STATUS_UPDATED
    campaignId: int
    orderId: int
    returnId: int
    statuses: NotificationUpdatedReturnStatusesDTO
    updatedAt: datetime


class OrderUpdatedNotificationDTO(BaseModel):
    notificationType: NotificationType.ORDER_UPDATED
    campaignId: int
    updateType: OrderUpdateType
    updatedAt: datetime


class GoodsFeedbackCreatedNotificationDTO(BaseModel):
    notificationType: NotificationType.GOODS_FEEDBACK_CREATED
    businessId: int
    createdAt: datetime
    feedbackId: int
    publishedAt: datetime


class GoodsFeedbackCommentCreatedNotificationDTO(BaseModel):
    notificationType: NotificationType.GOODS_FEEDBACK_COMMENT_CREATED
    businessId: int
    commentId: int
    createdAt: datetime


class ChatCreatedNotificationDTO(BaseModel):
    notificationType: NotificationType.CHAT_CREATED
    businessId: int
    chatId: int
    createdAt: datetime


class ChatMessageSentNotificationDTO(BaseModel):
    notificationType: NotificationType.CHAT_MESSAGE_SENT
    businessId: int
    chatId: int
    messageId: int
    sentAt: datetime


class ChatArbitrageStartedNotificationDTO(BaseModel):
    notificationType: NotificationType.CHAT_ARBITRAGE_STARTED
    businessId: int
    chatId: int
    startedAt: datetime


class ChatArbitrageFinishedNotificationDTO(BaseModel):
    notificationType: NotificationType.CHAT_ARBITRAGE_FINISHED
    businessId: int
    chatId: int
    finishedAt: datetime


class NotificationReturnItemDTO(BaseModel):
    count: int
    offerId: str





