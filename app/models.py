from __future__ import annotations

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Project(Base):
    __tablename__ = 'projects'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)

    scenes: Mapped[list[Scene]] = relationship(back_populates='project', cascade='all, delete-orphan')


class Scene(Base):
    __tablename__ = 'scenes'

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey('projects.id'), nullable=False)
    position: Mapped[int] = mapped_column(nullable=False, default=0)
    name: Mapped[str | None] = mapped_column(String(200))

    project: Mapped[Project] = relationship(back_populates='scenes')
    entries: Mapped[list[Entry]] = relationship(back_populates='scene', cascade='all, delete-orphan', order_by='Entry.position')


class Entry(Base):
    __tablename__ = 'entries'

    id: Mapped[int] = mapped_column(primary_key=True)
    scene_id: Mapped[int] = mapped_column(ForeignKey('scenes.id'), nullable=False)
    position: Mapped[int] = mapped_column(nullable=False, default=0)
    image_path: Mapped[str | None] = mapped_column(String(500))  # If the Entry came from a screenshot
    text: Mapped[str] = mapped_column(Text)  # NULL if OCR not yet run on image
    translation: Mapped[str | None] = mapped_column(Text)
    notes: Mapped[str | None] = mapped_column(Text)

    scene: Mapped[Scene] = relationship(back_populates='entries')
