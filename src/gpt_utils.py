from typing import Dict, Optional

import openai
from openai import OpenAI

from settings import MODEL_NAME, TEMPERATURE, OPENAI_TOKEN, \
    MAX_TOKENS_CONTEXT_OUTPUT, ORGANIZATION_ID

openai.api_key = OPENAI_TOKEN
client = OpenAI(
    organization=ORGANIZATION_ID
)


def get_answer(messages: Optional[Dict[str, str]] = None) -> str:
    """
    Get answer from OpenAI API.
    Parameters
    ----------
    messages:
        messages for OpenAI API
        Examples:
        >>> messages = {
        >>>     "prompt": "This is a test",
        >>>     "max_tokens": 5,
        >>>     "temperature": 1,

    Returns
    -------

    """
    ai_kwargs = {
        'model': MODEL_NAME,
        'messages': messages,
        'temperature': float(TEMPERATURE),
        'max_tokens': int(MAX_TOKENS_CONTEXT_OUTPUT)
    }
    completion = client.chat.completions.create(**ai_kwargs)
    return completion.choices[0].message.content


def get_gen_pic_url(text_description: str) -> str:
    response = client.images.generate(
        model="dall-e-3",
        prompt=text_description,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    return response.data[0].url
