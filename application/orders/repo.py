from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from application.database.models.order import Order


class OrderRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, order: Order) -> Order:
        """
        Create a new order.

        Репозиторий НЕ делает commit.
        flush нужен, чтобы получить PK/сгенерированные поля до commit.
        """
        self.session.add(order)
        await self.session.flush()
        return order

    async def get_by_id(self, order_id: int) -> Order | None:
        """
        Get an order by id.

        В 2.0 стиль: session.get() — самый простой и быстрый путь по PK.
        """
        return await self.session.get(Order, order_id)

    async def list(self, *, limit: int = 100, offset: int = 0) -> list[Order]:
        """
        List active orders with basic pagination.
        """
        stmt = (
            select(Order)
            .where(Order.is_active.is_(True))
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def delete(self, order: Order) -> None:
        """
        Delete an order (hard delete).

        Если тебе нужен soft delete — сделай order.is_active = False и flush.
        """
        await self.session.delete(order)
        await self.session.flush()
