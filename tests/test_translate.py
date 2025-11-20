from __future__ import annotations

import pytest

from app.services.translate import get_prompt, stream_translation


def test_get_prompt_doesnt_barf(example_scene):
    """Sanity test that this doesn't throw."""
    prompt = get_prompt(example_scene.entries[-1])
    assert prompt


@pytest.mark.asyncio
@pytest.mark.openai
async def test_stream_translation(example_scene):
    async for token in stream_translation(example_scene.entries[-1]):
        assert token
