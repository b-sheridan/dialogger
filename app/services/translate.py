from __future__ import annotations

from base64 import b64encode
from typing import AsyncGenerator

from openai import AsyncOpenAI

from app.config import OPENAI_API_KEY, OPENAI_MODEL
from app.models import Entry

SEPARATOR = '\x1f'

client = AsyncOpenAI(api_key=OPENAI_API_KEY)


async def stream_translation(entry: Entry) -> AsyncGenerator[str]:
    assert entry.text, 'Entry must have been created from text'

    prompt = [
        f'Translate a text from {entry.scene.project.name}.',
        'Return ONLY the translation for the last entry.',
    ]
    if entry.scene.name:
        prompt.append(f'Scene: {entry.scene.name}.')
    for other_entry in entry.scene.entries:
        prompt.append('-------')
        prompt.append(other_entry.text)

    stream = await client.responses.create(
        model=OPENAI_MODEL,
        input='\n'.join(prompt),
        stream=True,
    )

    async for event in stream:
        if event.type == 'response.output_text.delta':
            yield event.delta


async def stream_text_and_translation(entry: Entry) -> AsyncGenerator[tuple[str, str]]:
    assert entry.image_path, 'Entry must have been created from an image'

    prompt = [
        f'Extract and translate text from an image from {entry.scene.project.name}.',
        f'Between the extracted and translated text just insert this separator: {SEPARATOR}.',
        'The image is included with this request.',
        'Send me ONLY the extracted text and translated text; do not talk to me.',
    ]
    if len(entry.scene.entries) > 1:
        prompt.append('Previous scene context:')
        for number, prev_entry in enumerate(entry.scene.entries[:-1], 1):
            prompt.append(f'{number}. {prev_entry.text}')

    with open(entry.image_path, 'rb') as image_file:
        base64_image = b64encode(image_file.read()).decode('utf-8')

    stream = await client.responses.create(
        model=OPENAI_MODEL,
        stream=True,
        input=[
            {
                'role': 'user',
                'content': [
                    {
                        'type': 'input_text',
                        'text': '\n'.join(prompt)
                    },
                    {
                        'type': 'input_image',
                        'image_url': f'data:image/jpeg;base64,{base64_image}',
                    },
                ]
            },
        ],
    )

    sequence = 0
    text = ''
    translation = ''
    async for event in stream:
        if event.type == 'response.output_text.delta':
            if event.delta == SEPARATOR:
                sequence += 1
            elif sequence == 0:
                text += event.delta
            elif sequence == 1:
                translation += event.delta
            else:
                raise RuntimeError(f'invalid sequence {sequence}')
            yield (text, translation)
