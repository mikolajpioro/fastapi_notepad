from __future__ import annotations
from sqlalchemy import DateTime, Integer, String, Text
from datetime import UTC, datetime
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    date_posted: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))