import openai

from settings import MODEL_NAME, TEMPERATURE, MAX_TOKENS, OPENAI_TOKEN

openai.api_key = OPENAI_TOKEN


def get_answer(test):
    response = openai.Completion.create(
        model=MODEL_NAME,
        prompt=test,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS
    )
    return response['choices'][0]['text']
