from typing import Dict, Optional

import openai

from settings import MODEL_NAME, TEMPERATURE, MAX_TOKENS, OPENAI_TOKEN

openai.api_key = OPENAI_TOKEN


def get_answer(prompt: Optional[str] = None,
               messages: Optional[Dict[str, str]] = None) -> str:
    if prompt is not None:
        ai_kwargs = {
            'model': MODEL_NAME,
            'prompt': prompt,
            'temperature': TEMPERATURE,
            'max_tokens': MAX_TOKENS
        }
        api_resp = openai.Completion.create(
            **ai_kwargs
        )
        response = api_resp['choices'][0]['text']
    elif messages is not None:
        ai_kwargs = {
            'model': "gpt-3.5-turbo",
            'messages': messages
        }
        api_resp = openai.ChatCompletion.create(
            **ai_kwargs
        )
        response = api_resp['choices'][0]['message']['content']
    else:
        raise KeyError("at least one must be provided prompt or messages")
    return response


def get_gen_pic_url(text_description: str) -> str:
    response = openai.Image.create(
        prompt=text_description,
        n=1,
        size="1024x1024"
    )
    return response["data"][0]['url']
