from typing import TypeVar, Type, Generic, Mapping, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from application.orders.models.order_items import OrderItems
from application.orders.models.orders import Orders


T = TypeVar("T")

class BaseRepository(Generic[T]):
    model: type[T]

    @classmethod
    async def create(cls, session: AsyncSession, obj: T) -> T:
        """
        Create a new order.

        Репозиторий НЕ делает commit.
        flush нужен, чтобы получить PK/сгенерированные поля до commit.
        """
        session.add(obj)
        await session.flush()
        return obj

    @classmethod
    async def get_by_market_order_id(
            cls,
            session: AsyncSession,
            campaign_id: int,
            market_order_id: int,
    ) -> T | None:
        stmt = (
            select(cls.model)
            .where(
                cls.model.campaign_id == campaign_id,
                cls.model.market_order_id == market_order_id,
            )
        )
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    async def list(
        cls,
        session: AsyncSession,
        *,
        limit: int = 100,
        offset: int = 0,
    ) -> list[T]:
        """
        List active orders with pagination.
        """
        stmt = (
            select(T)
            .where(T.is_active.is_(True))
            .limit(limit)
            .offset(offset)
        )
        result = await session.execute(stmt)
        return list(result.scalars().all())

    @classmethod
    async def delete(
        cls,
        session: AsyncSession,
        obj: T,
    ) -> None:
        """
        Hard delete.
        """
        await session.delete(obj)
        await session.flush()

    @classmethod
    async def update(
            cls,
            session: AsyncSession,
            obj: T,
            data: Mapping[str, Any],
    ) -> T:
        """
        Update fields on an already loaded ORM object.
        """
        for key, value in data.items():
            setattr(obj, key, value)

        await session.flush()  # отправит UPDATE в БД в рамках транзакции
        await session.refresh(obj)  # опционально: подтянуть значения, выставленные БД (onupdate, триггеры)
        return obj

class OrderRepository(BaseRepository[Orders]):
    model = Orders

class OrderItemsRepository(BaseRepository[Orders]):
    model = OrderItems