from pydantic import BaseModel

from api.enums import *


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