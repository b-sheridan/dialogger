from __future__ import annotations

import pytest

from app.models import Entry, Scene, Project
from app.services.translate import stream_text_and_translation, stream_translation


@pytest.mark.asyncio
@pytest.mark.openai
async def test_stream_translation():
    project = Project(name='Xenogears')
    scene = Scene(project=project)
    entry1 = Entry(text='フェイ：やあ、アルル。それが花嫁のドレスかい？')
    entry2 = Entry(text='アルル：フェイ！？ ああ……、ビックリした！')
    scene.entries.append(entry1)
    scene.entries.append(entry2)

    async for text in stream_translation(entry2):
        entry2.text = text

    assert entry2.text


@pytest.mark.asyncio
@pytest.mark.openai
async def test_stream_text_and_translation():
    project = Project(name='Xenogears')
    scene = Scene(project=project)
    entry = Entry(scene=scene, image_path='tests/data/xenogears-320-240.png')

    async for (text, translation) in stream_text_and_translation(entry):
        entry.text = text
        entry.translation = translation

    assert entry.text
    assert entry.translation
