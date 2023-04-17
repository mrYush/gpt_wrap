import argparse
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


def get_kwargs(default_config_path: Path) -> argparse.ArgumentParser:
    r"""Kwargs parser for drill health and accident experiments launchers"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--config_path', metavar='</path/to/config>', type=lambda p: Path(p),
                        help=f'pass path to config.yaml\n'
                             f'Use {default_config_path}.example '
                             f'to create new config.yaml file',
                        default=default_config_path)
    parser.add_argument('-l', '--logger_level', metavar='<logger_level>', type=int,
                        help='NOTSET: 0, DEBUG: 10, INFO: 20, WARNING: 30, ERROR: 40, CRITICAL: 50',
                        default=20)
    return parser