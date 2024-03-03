"""Settings for the project."""
import os
from pathlib import Path


PROJECT_PATH = Path(__file__).parents[1]

MODEL_NAME = os.environ['MODEL_NAME']
TEMPERATURE = os.environ['TEMPERATURE']
# MAX_TOKENS = os.environ.get('MAX_TOKENS', default=config.get('MAX_TOKENS'))
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
OPENAI_TOKEN = os.environ['OPENAI_API_KEY']
MONGO_HOST = os.environ['MONGO_HOST']
MONGO_PORT = os.environ['MONGO_PORT']
MONGO_DATABASE = os.environ['MONGO_DATABASE']
MONGO_USERNAME = os.environ['MONGO_INITDB_ROOT_USERNAME']
MONGO_PASSWORD = os.environ['MONGO_INITDB_ROOT_PASSWORD']
MAX_TOKENS_CONTEXT_HISTORY = os.environ['MAX_TOKENS_CONTEXT_HISTORY']
MAX_TOKENS_CONTEXT_OUTPUT = os.environ['MAX_TOKENS_CONTEXT_OUTPUT']
ORGANIZATION_ID = os.environ['ORGANIZATION_ID']
TELEGRAM_ID_FOR_CONNECTION = os.environ['TELEGRAM_ID_FOR_CONNECTION']
MONGO_CREDS = {
    'db': MONGO_DATABASE,
    'host': MONGO_HOST,
    'port': int(MONGO_PORT),
    'username': MONGO_USERNAME,
    'password': MONGO_PASSWORD
}

ENCODING_HOST = os.environ.get('ENCODING_HOST', default=None)
ENCODING_PORT = os.environ.get('ENCODING_PORT', default=None)
if ENCODING_HOST and ENCODING_PORT:
    ENCODING_URL = f"http://{ENCODING_HOST}:{ENCODING_PORT}/encode_image"
else:
    ENCODING_URL = None
IMAGES_PATH = PROJECT_PATH / 'images'
