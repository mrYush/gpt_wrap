import json
import logging
import time

import openai
import requests
from openai import OpenAI

from settings import MODEL_NAME, TEMPERATURE, OPENAI_TOKEN, \
    MAX_TOKENS_CONTEXT_OUTPUT, ORGANIZATION_ID, URL

LOGGER = logging.getLogger()
openai.api_key = OPENAI_TOKEN
client = OpenAI(
    organization=ORGANIZATION_ID
)


def get_answer(messages: list[dict[str, str]]) -> str:
    """
    Get answer from OpenAI API.
    Parameters
    ----------
    messages: list[dict[str, str]]
        messages for api
        Examples:
        >>> messages = [
        >>>     {"role": "system",
        >>>      "content": "Useful assistant"},
        >>>     {"role": "user",
        >>>      "content": "Hello! What is tax?"},
        >>>     {"role": "context",
        >>>      "content": "Tax is ... <some text from database> ..."},
        >>>     {"role": "assistant",
        >>>      "content": "My name is John."},
        >>>     {"role": "user",
        >>>      "content": "What should I do if <some situation>?"},
        >>>     {"role": "context",
        >>>      "content": "<some text from database>"},
        >>>     {"role": "assistant",
        >>>      "content": "You should do <some action>."}
        >>> ]

    Returns
    -------
    str
    """
    # filtering only needed keys in each message
    messages = [
        {key: message[key] for key in ['role', 'content']}
        for message in messages
    ]
    payload = {
        'model': MODEL_NAME,
        'messages': messages,
        'temperature': float(TEMPERATURE),
        'max_tokens': int(MAX_TOKENS_CONTEXT_OUTPUT)
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_TOKEN}"
    }
    for counter in range(5):
        try:
            response = requests.post(url=URL, headers=headers,
                                     data=json.dumps(payload))
        except requests.exceptions.ConnectionError as exc:
            LOGGER.error(f"Connection error: {exc}")
            time.sleep(2)
            continue
        if response.status_code == 200:
            break
        LOGGER.error(f"Response status code: {response.status_code}")
        LOGGER.error(f"Response text: {response.text}")
    if response.status_code != 200:
        LOGGER.error(f"Response status code: {response.status_code}")
        LOGGER.error(f"Response text: {response.text}")
        return ("Что-то ко мне сегодня слишком много запросов, "
                "попробуйте написать чуть позже.")
    LOGGER.info(f"Got response from API: {response}")
    LOGGER.debug(f"Response json: {response.json()}")
    return response.json()['choices'][0]['message']['content']


def get_gen_pic_url(prompt: str) -> str:
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    return response.data[0].url
