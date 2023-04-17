import openai

from settings import MODEL_NAME, TEMPERATURE, MAX_TOKENS, OPENAI_TOKEN

openai.api_key = OPENAI_TOKEN


def get_answer(text: str) -> str:
    response = openai.Completion.create(
        model=MODEL_NAME,
        prompt=text,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS
    )
    return response['choices'][0]['text']


def get_gen_pic_url(text_description: str) -> str:
    response = openai.Image.create(
        prompt=text_description,
        n=1,
        size="1024x1024"
    )
    return response["data"][0]['url']
