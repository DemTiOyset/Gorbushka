from datetime import datetime
from typing import Optional, List

from sqlalchemy import (
    String, Integer, BigInteger, DateTime,
    UniqueConstraint, Index, Boolean
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from application.db import Base


class Orders(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)

    # --- Идентификация в Яндекс.Маркете (ключ к идемпотентности) ---
    campaign_id: Mapped[int] = mapped_column(Integer, nullable=False)
    market_order_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )
    last_event_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False)

    # --- Состояние заказа из уведомлений Маркета ---
    status: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    substatus: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)

    # --- Технические timestamps (когда мы записали/обновили в нашей БД) ---
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False,
    )

    is_returned: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    is_finished: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    order_items: Mapped[List["OrderItems"]] = relationship(
        "OrderItems",
        back_populates="order",
        cascade="all, delete, delete-orphan",
    )

    __table_args__ = (
        UniqueConstraint("campaign_id", "market_order_id", name="unique_campaign_id_market_order_id"),
        Index("ix_orders_market", "campaign_id", "market_order_id"),
    )
