from pathlib import Path
from typing import Dict, Any

import yaml


def get_yaml_config(path: Path) -> Dict[str, Any]:
    r"""Get anything what was in yaml. Probably dict"""
    with open(str(path)) as conf_file:
        exp_config = yaml.load(conf_file, Loader=yaml.Loader)
    return exp_config
