from __future__ import annotations

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Base, Entry, Project, Scene


# Use SQLite in-memory DB for tests
TEST_DATABASE_URL = 'sqlite:///:memory:'


def pytest_addoption(parser):
    parser.addoption(
        '--run-openai',
        action='store_true',
        default=False,
        help='Run tests which hit the OpenAI API',
    )


def pytest_configure(config):
    config.addinivalue_line('markers', 'openai: mark test as OpenAI')


def pytest_collection_modifyitems(config, items):
    if not config.getoption('--run-openai'):
        skip_openai = pytest.mark.skip(reason='use --run-openai to run')
        for item in items:
            if 'openai' in item.keywords:
                item.add_marker(skip_openai)


@pytest.fixture
def session():
    engine = create_engine(TEST_DATABASE_URL, future=True)
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

    # Create fresh schema for each test
    Base.metadata.create_all(bind=engine)

    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def example_scene(session):
    xenogears = Project(name='Xenogears')

    scene = Scene(
        project=xenogears,
        name='プロローグ、フェイとアルル',
        entries=[
            Entry(text="""フェイ：やあ、アルル。
それが花嫁のドレスかい？"""),
            Entry(text="""アルル：フェイ！？
ああ……、ビックリした！"""),
        ],
    )

    session.add(scene)
    session.commit()

    return scene
