from __future__ import annotations

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Title(Base):
    __tablename__ = 'titles'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)

    characters: Mapped[list[Character]] = relationship(back_populates='title', cascade='all, delete-orphan')
    scenes: Mapped[list[Scene]] = relationship(back_populates='title', cascade='all, delete-orphan')


class Character(Base):
    __tablename__ = 'characters'

    id: Mapped[int] = mapped_column(primary_key=True)
    title_id: Mapped[int] = mapped_column(ForeignKey('titles.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)

    title: Mapped[Title] = relationship(back_populates='characters')
    lines: Mapped[list[Line]] = relationship(back_populates='character')


class Scene(Base):
    __tablename__ = 'scenes'

    id: Mapped[int] = mapped_column(primary_key=True)
    title_id: Mapped[int] = mapped_column(ForeignKey('titles.id'), nullable=False)
    name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    position: Mapped[int] = mapped_column(nullable=False, default=0)

    title: Mapped[Title] = relationship(back_populates='scenes')
    lines: Mapped[list[Line]] = relationship(back_populates='scene', cascade='all, delete-orphan', order_by='Line.position')


class Line(Base):
    __tablename__ = 'lines'

    id: Mapped[int] = mapped_column(primary_key=True)
    scene_id: Mapped[int] = mapped_column(ForeignKey('scenes.id'), nullable=False)
    character_id: Mapped[int | None] = mapped_column(ForeignKey('characters.id'))
    position: Mapped[int] = mapped_column(nullable=False, default=0)
    original_text: Mapped[str] = mapped_column(Text, nullable=False)
    translated_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    scene: Mapped[Scene] = relationship(back_populates='lines')
    character: Mapped[Character] = relationship(back_populates='lines')
