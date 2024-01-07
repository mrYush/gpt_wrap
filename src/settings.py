"""Settings for the project."""
import os
from pathlib import Path


PROJECT_PATH = Path(__file__).parent.parent

MODEL_NAME = os.environ.get('MODEL_NAME', default='davinci')
TEMPERATURE = os.environ.get('TEMPERATURE', default=0.9)
# MAX_TOKENS = os.environ.get('MAX_TOKENS', default=config.get('MAX_TOKENS'))
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
OPENAI_TOKEN = os.environ.get('OPENAI_TOKEN')
MONGO_HOST = os.environ['MONGO_HOST']
MONGO_PORT = os.environ['MONGO_PORT']
MONGO_DATABASE = os.environ['MONGO_DATABASE']
MONGO_USERNAME = os.environ['MONGO_INITDB_ROOT_USERNAME']
MONGO_PASSWORD = os.environ['MONGO_INITDB_ROOT_PASSWORD']
MAX_TOKENS_CONTEXT_HISTORY = os.environ.get('MAX_TOKENS_CONTEXT_HISTORY')
MAX_TOKENS_CONTEXT_OUTPUT = os.environ.get('MAX_TOKENS_CONTEXT_OUTPUT')
ORGANIZATION_ID = os.environ.get('ORGANIZATION_ID')
TELEGRAM_ID_FOR_CONNECTION = os.environ.get('TELEGRAM_ID_FOR_CONNECTION')
MONGO_CREDS = {
    'db': MONGO_DATABASE,
    'host': MONGO_HOST,
    'port': int(MONGO_PORT),
    'username': MONGO_USERNAME,
    'password': MONGO_PASSWORD
}
