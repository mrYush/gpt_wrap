"""Settings for the project."""
import os
from pathlib import Path

AI_CONFIG_NAME = 'config.yaml'
PROJECT_PATH = Path(__file__).parent.parent

MODEL_NAME = os.environ['MODEL_NAME']
TEMPERATURE = os.environ['TEMPERATURE']
# MAX_TOKENS = os.environ.get('MAX_TOKENS', default=config.get('MAX_TOKENS'))
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
OPENAI_TOKEN = os.environ['OPENAI_TOKEN']
MONGO_HOST = os.environ['MONGO_HOST']
MAX_TOKENS_CONTEXT_HISTORY = os.environ['MAX_TOKENS_CONTEXT_HISTORY']
MAX_TOKENS_CONTEXT_OUTPUT = os.environ['MAX_TOKENS_CONTEXT_OUTPUT']
ORGANIZATION_ID = os.environ['ORGANIZATION_ID']