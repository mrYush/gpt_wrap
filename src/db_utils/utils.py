from typing import Dict, List


def get_several_keys(item: Dict, keys: List[str]) -> dict:
    """Get several pair key value from dict"""
    return {key: item[key] for key in keys}
