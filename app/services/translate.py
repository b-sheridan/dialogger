from __future__ import annotations

from typing import AsyncGenerator

from openai import AsyncOpenAI

from app.config import OPENAI_API_KEY, OPENAI_MODEL
from app.models import Entry

client = AsyncOpenAI(api_key=OPENAI_API_KEY)


def get_prompt(entry: Entry) -> str:
    parts = [
        f'Translate a text from {entry.scene.project.name}.',
        'Return ONLY the translation for the last entry.',
    ]
    if entry.scene.name:
        parts.append(f'Scene: {entry.scene.name}.')
    for other_entry in entry.scene.entries:
        parts.append('-------')
        parts.append(other_entry.text)
    return '\n'.join(parts)


async def stream_translation(entry: Entry) -> AsyncGenerator[str]:
    prompt = get_prompt(entry)
    stream = await client.responses.create(model=OPENAI_MODEL, input=prompt, stream=True)
    async for event in stream:
        match event.type:
            case 'response.output_text.delta':
                yield event.delta
            case 'response.created' | 'response.in_progress' | 'response.output_item.added' | 'response.content_part.added':
                pass  # nothing to do, we're just waiting
            case 'response.output_text.done':
                return  # done
            case _:
                raise NotImplementedError(event)
