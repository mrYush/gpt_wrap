"""Utils for db_utils"""
from typing import Dict, List


def get_several_keys(item: Dict, keys: List[str]) -> dict:
    """
    Get several pair key value from dict
    Parameters
    ----------
    item: Dict[Any, Any]
        dict from which we want to get several keys
    keys: List[Any]
        list of keys wich need to be saved in new dict

    Returns
    -------
        dict
    """
    return {key: item[key] for key in keys}
