"""
Module for getting some statistics
"""
from db_utils.scheme import UsersCollection, ConversationCollection, \
    PictureCollection


def get_all_users() -> list[dict]:
    """
    Get all users from db
    Returns
    -------
        list of users
    """
    return list(UsersCollection.objects().all())


def get_all_messages() -> list[dict]:
    """
    Get all messages from db
    Returns
    -------
        list of messages
    """
    return list(ConversationCollection.objects(
        role='user'
    ).all())


def get_all_pictures() -> list[dict]:
    """
    Get all pictures from db
    Returns
    -------
        list of pictures
    """
    return list(PictureCollection.objects().all())
