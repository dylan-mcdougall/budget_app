"""Transaction category model for organizing transactions."""
from enum import Enum
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from .budget import Budget
    from .transaction import Transaction
    from .user import User


class CategoryType(str, Enum):
    """Type of transaction category."""
    INCOME = "income"
    EXPENSE = "expense"


class TransactionCategory(Base, UUIDMixin, TimestampMixin):
    """Category for organizing transactions."""

    __tablename__ = "transaction_categories"

    user_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        index=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    category_type: Mapped[CategoryType] = mapped_column(nullable=False)
    color: Mapped[Optional[str]] = mapped_column(String(7), nullable=True)  # Hex color code
    icon: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    is_system: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # Self-referential for subcategories
    parent_category_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("transaction_categories.id", ondelete="CASCADE"),
        nullable=True
    )

    # Relationships
    user: Mapped[Optional["User"]] = relationship("User", back_populates="categories")
    parent_category: Mapped[Optional["TransactionCategory"]] = relationship(
        "TransactionCategory",
        remote_side="TransactionCategory.id",
        back_populates="subcategories"
    )
    subcategories: Mapped[list["TransactionCategory"]] = relationship(
        "TransactionCategory",
        back_populates="parent_category",
        cascade="all, delete-orphan"
    )
    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction",
        back_populates="category"
    )
    budgets: Mapped[list["Budget"]] = relationship(
        "Budget",
        back_populates="category",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<TransactionCategory(id={self.id}, name={self.name}, type={self.category_type})>"
