from typing import List, Optional

from pydantic import BaseModel, ConfigDict


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
