import logging
from datetime import datetime
from typing import Optional

import tiktoken
from mongoengine import Document, StringField, IntField, connect, \
    BooleanField, FloatField
from telegram import User

from db_utils.utils import get_several_keys
from settings import MONGO_HOST, MODEL_NAME, MAX_TOKENS_CONTEXT_HISTORY

LOGGER = logging.getLogger()

connect(alias='users', db='my_database', host=MONGO_HOST)
connect(alias='requests', db='my_database', host=MONGO_HOST)
connect(alias='context', db='my_database', host=MONGO_HOST)


class SystemContext(Document):
    context_alias = StringField()
    context = StringField()
    meta = {'db_alias': 'context'}


class UsersCollection(Document):
    telegram_id = IntField(required=True)
    first_name = StringField()
    last_name = StringField()
    username = StringField()
    is_bot = BooleanField()
    current_context = IntField()
    start_context_timestamp = FloatField()
    system_prompt = StringField()
    limit_msg = IntField()
    limit_pic = IntField()
    meta = {'db_alias': 'users'}


class ConversationCollection(Document):
    telegram_id = IntField(required=True)
    context_id = IntField()
    role = StringField()
    content = StringField()
    timestamp = FloatField()
    meta = {'db_alias': 'requests'}


class PictureCollection(Document):
    telegram_id = IntField(required=True)
    prompt = StringField()
    url = StringField()
    timestamp = FloatField()
    meta = {'db_alias': 'requests'}


def check_user(user: User, return_mongo_user: bool = False):
    possible_users = UsersCollection.objects(telegram_id=user.id)
    if (len(possible_users) == 1) and return_mongo_user:
        return possible_users[0]
    elif len(possible_users) == 1:
        return True
    elif len(possible_users) == 0:
        msg = f"User {user.id}, {user.full_name} wasn't exist. Creating..."
        LOGGER.warning(msg)
        cur_timestamp = datetime.now().timestamp()
        new_user = UsersCollection(
            telegram_id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            start_context_timestamp=cur_timestamp,
            is_bot=user.is_bot,
            limit_msg=30,
            limit_pic=10
        )
        new_user.save()
        if return_mongo_user:
            return new_user
    elif len(possible_users) > 1:
        msg = f"There are several users: {user.id}, {user.full_name}"
        LOGGER.warning(msg)
        return False
    else:
        raise KeyError(f"Impossible user's count {len(possible_users)}")


def set_current_context(user: User, context_name: str) -> Optional[int]:
    """
    Method for setting context in UsersCollection
    Parameters
    ----------
    user: User
        telegram user
    context_name: str
        context_name

    Returns
    -------
    context_num
    """
    if 'context' not in context_name:
        msg = f"context_name must contains 'context', got {context_name}"
        raise ValueError(msg)
    mongo_user = check_user(user=user, return_mongo_user=True)
    if 'purge' in context_name:
        mongo_user.update(start_context_timestamp=datetime.now().timestamp())
        return mongo_user.current_context
    context_num = int(context_name.split('_')[1])
    if context_num == 0:
        context_num = None
    mongo_user.update(current_context=context_num)
    return context_num


def num_tokens_from_string(string: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(MODEL_NAME)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def get_last_messages(
        user_id: int,
        tokens: int = int(MAX_TOKENS_CONTEXT_HISTORY),
        system_prompt: Optional[str] = None,
        start_from_timestamp: Optional[int] = None
) -> list[dict[str, str]]:
    """
    Get last messages from user's conversation history. All message will
    be less than tokens. If system_prompt exists, it will be added.
    Parameters
    ----------
    user_id: int
        telegram user id
    tokens: int
        max number of tokens in all messages
    system_prompt: Optional[str]
        system prompt
    start_from_timestamp: Optional[int]
        timestamp when context was purged last time
    Returns
    -------
    list of messages
    Examples:
    >>> get_last_messages(user_id=123456789, tokens=1000,
    >>>                   system_prompt='system prompt')
    [{'role': 'system', 'content': 'system prompt'},
     {'role': 'user', 'content': 'user message'}]
    """
    all_messages = ConversationCollection.objects(telegram_id=user_id)
    all_messages_list = [{'role': msg.role, 'content': msg.content,
                          'timestamp': msg.timestamp}
                         for msg in all_messages]

    all_messages_list_sorted = sorted(all_messages_list,
                                      key=lambda d: d['timestamp'],
                                      reverse=True)
    if start_from_timestamp is None:
        start_from_timestamp = all_messages_list_sorted[-1]['timestamp']
    filtered_messages = list()
    massage_length = 0 if system_prompt is None else num_tokens_from_string(
        system_prompt)

    for message in all_messages_list_sorted:
        this_message_length = num_tokens_from_string(message['content'])
        massage_length += this_message_length
        too_long_context = (massage_length + this_message_length) > tokens
        too_long_ago = message['timestamp'] < start_from_timestamp
        if too_long_context or too_long_ago:
            if system_prompt is not None:
                filtered_messages.append(
                    {'role': 'system', 'content': system_prompt}
                )
            break
        filtered_messages.append(
            get_several_keys(item=message, keys=['role', 'content'])
        )

    if len(filtered_messages) == 0:
        filtered_messages.append({'role': 'system', 'content': 'no context'})
    filtered_messages.reverse()
    return filtered_messages
