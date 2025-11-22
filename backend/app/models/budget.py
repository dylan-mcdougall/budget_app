"""Budget model for financial planning and spending limits."""
from datetime import date
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import Date, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from .category import TransactionCategory
    from .user import User


class BudgetPeriod(str, Enum):
    """Budget period types."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"


class Budget(Base, UUIDMixin, TimestampMixin):
    """Budget model for tracking spending limits per category."""

    __tablename__ = "budgets"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    category_id: Mapped[UUID] = mapped_column(
        ForeignKey("transaction_categories.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    amount: Mapped[Decimal] = mapped_column(
        Numeric(precision=15, scale=2),
        nullable=False
    )
    period: Mapped[BudgetPeriod] = mapped_column(nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="budgets")
    category: Mapped["TransactionCategory"] = relationship(
        "TransactionCategory",
        back_populates="budgets"
    )

    def __repr__(self) -> str:
        return f"<Budget(id={self.id}, amount={self.amount}, period={self.period})>"
