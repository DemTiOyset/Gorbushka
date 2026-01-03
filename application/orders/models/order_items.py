from datetime import date, datetime
from typing import Optional

from sqlalchemy import Date, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import mapped_column, Mapped, relationship

from application.db import Base


class OrderItems(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)

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

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
    )

    order: Mapped["Orders"] = relationship(
        "Orders",
        back_populates="order_items",
    )