from datetime import datetime
from http.client import responses
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from application.orders.shemas.enums import *

class CreateOrderDTO(BaseModel):
    """CreateOrderDTO"""
    model_config = ConfigDict(use_enum_values=True, populate_by_name=True)
    campaign_id: int = Field(alias="campaignId")
    market_order_id: int = Field(alias="orderId")
    event_time: Optional[str] = None
    status: Optional[OrderStatusType] = OrderStatusType.PENDING
    substatus: Optional[str] = None
    product_name: Optional[str] = None
    quantity: Optional[int] = Field(alias="count", default=None)
    price_from_market: Optional[float] = None
    market_commission: Optional[float] = None
    market_costs: Optional[float] = Field(alias="value", default=None)
    discount: Optional[float] = None
    shipping_date: Optional[str] = None
    preliminary_costs: Optional[float] = None

class UpdateOrderDTO(BaseModel):
    """UpdateOrderDTO"""



