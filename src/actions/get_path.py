import os
import pathlib

import yaml

DATA_PATH_DEFAULT_KEY = "data_path"
MODELS_PATH_DEFAULT_KEY = "models_path"


def get_base_config_path():
    return pathlib.Path(__file__).parents[2] / "config.yaml"


def load_config_from_yaml(config=None):
    if not config:
        config = get_base_config_path()
    with open(config, "r") as f:
        return yaml.load(f, Loader=yaml.Loader)


def get_data_path(config=None):
    config_data = load_config_from_yaml(config=config)
    return pathlib.Path(config_data[DATA_PATH_DEFAULT_KEY])


def get_models_path(config=None):
    config_data = load_config_from_yaml(config=config)
    return pathlib.Path(config_data[MODELS_PATH_DEFAULT_KEY])
