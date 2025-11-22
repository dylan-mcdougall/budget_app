"""Transaction model for financial transactions."""
from datetime import date
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import Date, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from .account import Account
    from .category import TransactionCategory


class TransactionType(str, Enum):
    """Type of transaction."""
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"


class Transaction(Base, UUIDMixin, TimestampMixin):
    """Financial transaction model."""

    __tablename__ = "transactions"

    account_id: Mapped[UUID] = mapped_column(
        ForeignKey("accounts.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    category_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("transaction_categories.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    amount: Mapped[Decimal] = mapped_column(
        Numeric(precision=15, scale=2),
        nullable=False
    )
    transaction_type: Mapped[TransactionType] = mapped_column(nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    transaction_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # For transfers: link to the corresponding transaction in the destination account
    linked_transaction_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("transactions.id", ondelete="SET NULL"),
        nullable=True
    )

    # Relationships
    account: Mapped["Account"] = relationship("Account", back_populates="transactions")
    category: Mapped[Optional["TransactionCategory"]] = relationship(
        "TransactionCategory",
        back_populates="transactions"
    )
    linked_transaction: Mapped[Optional["Transaction"]] = relationship(
        "Transaction",
        remote_side="Transaction.id"
    )

    def __repr__(self) -> str:
        return f"<Transaction(id={self.id}, amount={self.amount}, type={self.transaction_type})>"
