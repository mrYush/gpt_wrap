import logging
from pathlib import Path
from typing import Dict, Any, Optional

import yaml


def get_yaml_config(path: Path) -> Dict[str, Any]:
    r"""Get anything what was in yaml. Probably dict"""
    with open(str(path)) as conf_file:
        exp_config = yaml.load(conf_file, Loader=yaml.Loader)
    return exp_config


def get_logger(logger_name: Optional[str] = None, path: Optional[Path] = None,
               level: int = logging.DEBUG) -> logging.Logger:
    """
    Logger initializing
    """
    logger_name = 'logs' if logger_name is None else logger_name
    path_to_logs = Path('logs') if path is None else Path(path)
    path_to_logs.mkdir(parents=True, exist_ok=True)
    filename = path_to_logs / f'{logger_name}.log'
    print(f'Log file path: {filename}')
    logging.basicConfig(level=level,
                        format=u'%(levelname)-8s [%(asctime)s] %(message)s',
                        filename=filename)
    logger = logging.getLogger(logger_name)
    return logger
