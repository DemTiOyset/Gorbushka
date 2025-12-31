from datetime import datetime, date
from typing import Optional

from sqlalchemy import (
    String, Integer, BigInteger, Numeric, Date, DateTime,
    UniqueConstraint, Index, func, text
)
from sqlalchemy.orm import Mapped, mapped_column

from application.db import Base


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)

    # --- Идентификация в Яндекс.Маркете (ключ к идемпотентности) ---
    campaign_id: Mapped[int] = mapped_column(Integer, nullable=False)
    market_order_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    event_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    # --- Состояние заказа из уведомлений Маркета ---
    status: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    substatus: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)

    # --- Твои бизнес-поля (примерно из того, что ты перечислил) ---
    product_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    quantity: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    shipping_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    # Деньги: лучше Numeric, а не float (float даёт ошибки округления)
    price_from_market: Mapped[Optional[float]] = mapped_column(Numeric(14, 2), nullable=True)
    market_commission: Mapped[Optional[float]] = mapped_column(Numeric(14, 2), nullable=True)
    market_costs: Mapped[Optional[float]] = mapped_column(Numeric(14, 2), nullable=True)
    discount: Mapped[Optional[float]] = mapped_column(Numeric(14, 2), nullable=True)
    preliminary_costs: Mapped[Optional[float]] = mapped_column(Numeric(14, 2), nullable=True)

    # --- Технические timestamps (когда мы записали/обновили в нашей БД) ---
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text('(now() at time zone "utc")'),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text('(now() at time zone "utc")'),
        onupdate=func.now(),
        nullable=False,
    )

    __table_args__ = (
        Index("ix_orders_market", "campaign_id", "market_order_id"),
    )
