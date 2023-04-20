import logging
from datetime import datetime
from typing import Optional

import pandas as pd
from mongoengine import Document, StringField, IntField, connect, BooleanField, FloatField
from telegram import User

from settings import MONGO_HOST

LOGGER = logging.getLogger()

connect(alias='users', db='my_database', host=MONGO_HOST)
connect(alias='requests', db='my_database', host=MONGO_HOST)
connect(alias='context', db='my_database', host=MONGO_HOST)


class SystemContext(Document):
    context_id = IntField(required=True)
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
    meta = {'db_alias': 'users'}


class ConversationCollection(Document):
    telegram_id = IntField(required=True)
    context_id = IntField()
    role = StringField()
    content = StringField()
    timestamp = FloatField()
    meta = {'db_alias': 'requests'}


def check_user(user: User, return_mongo_user: bool=False):
    possible_users = UsersCollection.objects(telegram_id=user.id)
    if (len(possible_users) == 1) and return_mongo_user:
        return possible_users[0]
    elif len(possible_users) == 1:
        return True
    elif len(possible_users) == 0:
        msg = f"User {user.id}, {user.full_name} wasn't exist. Creating..."
        LOGGER.warning(msg)
        UsersCollection(telegram_id=user.id, first_name=user.first_name,
                        last_name=user.last_name, username=user.username,
                        is_bot=user.is_bot).save()
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


def get_last_n_message(user_id: int, count: int):
    all_messages = ConversationCollection.objects(telegram_id=user_id)
    conversation = pd.DataFrame.from_dict([
        {'role': msg.role, 'content': msg.content, 'timestamp': msg.timestamp}
        for msg in all_messages
    ]).sort_values('timestamp', ascending=True).tail(count * 2)
    users = possible_users = UsersCollection.objects(telegram_id=user_id)
    if len(users) == 1:
        user = users[0]
    else:
        raise KeyError(f"wrong userd. Please check user_id {user_id}")
    conversation = conversation[conversation['timestamp'] > user.start_context_timestamp]
    return conversation[['role', 'content']].to_dict(orient='records')
