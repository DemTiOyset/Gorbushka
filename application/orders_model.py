from datetime import datetime

from sqlalchemy import String, INTEGER, FLOAT, DATE
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True,)

    product_name: Mapped[str] = mapped_column(
        String(255),
    )

    quantity: Mapped[int] = mapped_column(INTEGER)

    price_from_market: Mapped[float] = mapped_column(FLOAT)

    market_commission: Mapped[float] = mapped_column(FLOAT)

    market_costs: Mapped[float] = mapped_column(FLOAT)

    discount: Mapped[float] = mapped_column(FLOAT)

    product_series: Mapped[str] = mapped_column(
        String(255)
    )

    shipping_date: Mapped[datetime] = mapped_column(DATE)

    preliminary_costs: Mapped[float] = mapped_column(FLOAT)


