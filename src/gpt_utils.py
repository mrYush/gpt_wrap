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
    ai_kwargs = {
        'model': MODEL_NAME,
        'messages': messages,
        'temperature': TEMPERATURE,
        'max_tokens': MAX_TOKENS_CONTEXT_OUTPUT
    }
    api_resp = openai.ChatCompletion.create(
        **ai_kwargs
    )
    response = api_resp['choices'][0]['message']['content']
    return response


def get_gen_pic_url(text_description: str) -> str:
    response = client.images.generate(
        model="dall-e-3",
        prompt=text_description,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    return response["data"][0]['url']
