from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from application.orders.models.order import Order


class OrderRepository:
    @classmethod
    async def create(cls, session: AsyncSession, order: Order) -> Order:
        """
        Create a new order.

        Репозиторий НЕ делает commit.
        flush нужен, чтобы получить PK/сгенерированные поля до commit.
        """
        session.add(order)
        await session.flush()
        return order

    @classmethod
    async def get_by_id(
        cls,
        session: AsyncSession,
        order_id: int,
    ) -> Order | None:
        """
        Get order by PK.
        """
        return await session.get(Order, order_id)

    @classmethod
    async def list(
        cls,
        session: AsyncSession,
        *,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Order]:
        """
        List active orders with pagination.
        """
        stmt = (
            select(Order)
            .where(Order.is_active.is_(True))
            .limit(limit)
            .offset(offset)
        )
        result = await session.execute(stmt)
        return list(result.scalars().all())

    @classmethod
    async def delete(
        cls,
        session: AsyncSession,
        order: Order,
    ) -> None:
        """
        Hard delete.
        """
        await session.delete(order)
        await session.flush()
