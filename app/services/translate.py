from __future__ import annotations

from typing import AsyncGenerator

from openai import AsyncOpenAI

from app.config import OPENAI_API_KEY, OPENAI_MODEL
from app.models import Line

client = AsyncOpenAI(api_key=OPENAI_API_KEY)


def get_prompt(line: Line) -> str:
    parts = [
        f'Translate a line of dialog from {line.scene.title.name}.',
        'Return ONLY the translation for the last line of dialog.',
    ]
    if line.scene.name:
        parts.append(f'Scene: {line.scene.name}.')
    for dialog in line.scene.lines:
        parts.append('-------')
        if dialog.character and dialog.character.name:
            parts.append(f'{dialog.character.name}: {dialog.original_text}')
        else:
            parts.append(dialog.original_text)
    return '\n'.join(parts)


async def stream_translation(line: Line) -> AsyncGenerator[str]:
    prompt = get_prompt(line)
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
