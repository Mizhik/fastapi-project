from uuid import UUID
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy import ForeignKey, String, Integer, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from model.base_model import Base
from model.enums import Gender


class User(Base):
    __tablename__ = "users"
    fullname: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    sex: Mapped[Gender] = mapped_column("sex", Enum(Gender), default=None)

    pets: Mapped[list["Pet"]] = relationship(
        "Pet", back_populates="owner", lazy="selectin", cascade="all, delete-orphan"
    )


class Pet(Base):
    __tablename__ = "pets"
    nickname: Mapped[str] = mapped_column(String(255), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    sex: Mapped[Gender] = mapped_column("sex", Enum(Gender), default=None)

    owner_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    owner: Mapped["User"] = relationship("User", back_populates="pets")
