import os
from pathlib import Path

from scrip_utils import get_yaml_config

AI_CONFIG_NAME = 'config.yaml'
PROJECT_PATH = Path(__file__).parent.parent
config_path = PROJECT_PATH / AI_CONFIG_NAME

config = get_yaml_config(path=config_path)
MODEL_NAME = os.environ.get('MODEL_NAME', default=config.get('MODEL_NAME'))
TEMPERATURE = os.environ.get('TEMPERATURE', default=config.get('TEMPERATURE'))
MAX_TOKENS = os.environ.get('MAX_TOKENS', default=config.get('MAX_TOKENS'))
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN', default=config.get('TELEGRAM_TOKEN'))
OPENAI_TOKEN = os.environ.get('OPENAI_TOKEN', default=config.get('OPENAI_TOKEN'))
MONGO_HOST = os.environ.get('MONGO_HOST', default=config.get('MONGO_HOST', 'localhost'))
MAX_TOKENS_CONTEXT_HISTORY = os.environ.get('MAX_TOKENS_CONTEXT_HISTORY',
                                            default=config.get('MAX_TOKENS_CONTEXT_HISTORY', 1800))
MAX_TOKENS_CONTEXT_OUTPUT = os.environ.get('MAX_TOKENS_CONTEXT_OUTPUT',
                                           default=config.get('MAX_TOKENS_CONTEXT_OUTPUT', 1000))
