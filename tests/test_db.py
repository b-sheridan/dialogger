from __future__ import annotations

from app.models import Project


def test_can_insert_and_query_project(session):
    # Insert a row
    project = Project(name='Test Project')
    session.add(project)
    session.commit()
    session.refresh(project)

    # Query it back
    result = session.query(Project).get(project.id)

    assert result is not None
    assert result.name == 'Test Project'
    assert result.id


def test_example_scene(example_scene):
    assert example_scene.id is not None
    assert example_scene.entries != []
