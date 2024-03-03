"""This module contains the function to initialize the database"""
import logging

from db_utils.scheme import SystemContext
from db_utils.utils import get_several_keys
from system_prompts.prompts import SYSTEM_PROMPTS

LOGGER = logging.getLogger()


def init_db():
    """Initializes the database with the system prompts"""
    existed_prompts = [get_several_keys(sc, ['context_alias', 'context'])
                       for sc in SystemContext.objects.all()]
    for prompt in SYSTEM_PROMPTS:
        if prompt in existed_prompts:
            LOGGER.warning(f"Prompt {prompt['context_alias']} already exists")
            continue
        SystemContext(
            context_alias=prompt['context_alias'],
            context=prompt['context']
        ).save()
