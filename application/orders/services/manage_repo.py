from sqlalchemy.ext.asyncio import AsyncSession

from application.db import async_session_maker
from application.orders.models.order_items import OrderItems
from application.orders.models.orders import Orders
from application.orders.repo import OrderRepository
from application.orders.shemas.notifications import BusinessOrderDTO
from application.orders.shemas.orders import OrderDTO, CreateOrderItemsDTO


async def create_order_with_items(
        order_dto: OrderDTO,
        items_dto: list[CreateOrderItemsDTO]
) -> Orders:
    order = dto_to_order(order_dto)
    order.order_items = [dto_to_order_item(dto) for dto in items_dto]

    async with async_session_maker() as session:
        async with session.begin():
            session.add(order)

            await session.flush()
            await session.refresh(order)

            return order

async def update_order_status(order_dto: OrderDTO) -> Orders:
    async with async_session_maker() as session:
        async with session.begin():
            order = await _update_order_status(order_dto=order_dto, session=session)

            if order is None:
                return None
            order.is_finished = True
            order.is_returned = True

            await session.flush()
            await session.refresh(order)

            return order


async def update_cancelled_order(order_dto: OrderDTO) -> Orders:
    async with async_session_maker() as session:
        async with session.begin():
            order = await _update_order_status(order_dto=order_dto, session=session)

            if order is None:
                return None

            await session.flush()
            await session.refresh(order)

            return order

async def update_return_status(order_dto: OrderDTO) -> Orders:
    async with async_session_maker() as session:
        async with session.begin():
            order = await _update_order_status(order_dto=order_dto, session=session)

            if order is None:
                return None

            order.is_finished = True
            order.is_returned = True

            await session.flush()
            await session.refresh(order)

            return order

async def update_order_shipment_date(order_data: BusinessOrderDTO) -> Orders:
    async with async_session_maker() as session:
        async with session.begin():
            order_id = order_data.orderId
            shipment_date = order_data.delivery.shipment.shipmentDate
            order = await OrderRepository.update_shipment_date(
                session=session,
                order_id=order_id,
                shipment_date=shipment_date
            )

            return order

async def _update_order_status(order_dto: OrderDTO, session: AsyncSession) -> Orders:
        order = await OrderRepository.get_by_market_order_id(
            session=session,
            campaign_id=order_dto.campaign_id,
            market_order_id=order_dto.market_order_id,
        )

        if order is None:
            return None

        if order_dto.last_event_time is not None and order.last_event_time is not None:
            if order_dto.last_event_time <= order.last_event_time:
                return order

        order.status = order_dto.status
        order.substatus = order_dto.substatus
        order.last_event_time = order_dto.last_event_time

        return order

def dto_to_order(dto: OrderDTO) -> Orders:
    return Orders(
        campaign_id=dto.campaign_id,
        market_order_id=dto.market_order_id,
        status=dto.status,
        substatus=dto.substatus,
        last_event_time=dto.last_event_time,
    )

def dto_to_order_item(dto: CreateOrderItemsDTO) -> OrderItems:
    return OrderItems(
        product_name=dto.product_name,
        quantity=dto.quantity,
        price_from_market=dto.price_from_market,
        market_commission=dto.market_commission,
        market_costs=dto.market_costs,
        discount=dto.discount,
        shipping_date=dto.shipping_date,
    )

