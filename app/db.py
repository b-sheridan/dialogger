from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import DATABASE_URL
from app.models import Base

if not DATABASE_URL:
    raise RuntimeError('DATABASE_URL is not set')

# SQLAlchemy engine (sync)
engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True,
)


# Session factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)
