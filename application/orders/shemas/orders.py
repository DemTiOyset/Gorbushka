from datetime import datetime
from http.client import responses
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, AliasChoices

from application.orders.shemas.enums import *

class OrderDTO(BaseModel):
    """CreateOrderDTO"""
    model_config = ConfigDict(use_enum_values=True, populate_by_name=True)
    campaign_id: int | None = Field(alias="campaignId", default=None)
    market_order_id: int | None = Field(alias="orderId", default=None)
    last_event_time: datetime | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "createdAt",
            "updatedAt",
            "cancelledAt"
        ),
        serialization_alias="event_time"
    )
    status: str | None = None
    substatus: str | None = None


class CreateOrderItemsDTO(BaseModel):
    """CreateOrderDTO"""
    model_config = ConfigDict(use_enum_values=True, populate_by_name=True)
    product_name: str | None = None
    quantity: int | None = Field(alias="count", default=None)
    price_from_market: float | None = None
    market_commission: float | None = None
    market_costs: float | None = Field(alias="value", default=None)
    discount: float | None = None
    shipping_date: datetime | None = None
    preliminary_costs: float | None = None
