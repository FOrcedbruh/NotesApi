from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .note import Note


class User(Base):
    __tablename__ = "users"
    
    username: Mapped[str] = mapped_column(String(12), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False)
    gender: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[bytes] = mapped_column(nullable=False)
    
    posts: Mapped[list["Note"]] = relationship(back_populates="user")
    
    
    