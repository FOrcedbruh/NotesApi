from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from .base import Base
import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User



class Note(Base):
    __tablename__ = "notes"
    
    title: Mapped[str] = mapped_column(String(10), default="", server_default="")
    body: Mapped[str] = mapped_column(String)
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="posts")