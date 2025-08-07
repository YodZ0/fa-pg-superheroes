from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.models.base import Base


class Superhero(Base):
    __tablename__ = "superheroes"

    id: Mapped[int] = mapped_column(
        Integer,
        index=True,
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[str] = mapped_column(String, unique=True)
    intelligence: Mapped[int] = mapped_column(Integer)
    strength: Mapped[int] = mapped_column(Integer)
    speed: Mapped[int] = mapped_column(Integer)
    durability: Mapped[int] = mapped_column(Integer)
    power: Mapped[int] = mapped_column(Integer)
    combat: Mapped[int] = mapped_column(Integer)
