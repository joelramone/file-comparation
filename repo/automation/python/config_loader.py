from __future__ import annotations

from pathlib import Path

import yaml

from .exceptions import ConfigError
from .models import MappingConfig, Settings


def _read_yaml(path: Path) -> dict:
    if not path.exists():
        raise ConfigError(f"Configuration file not found: {path}")
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ConfigError(f"Invalid YAML object in {path}")
    return data


def load_settings(path: Path) -> Settings:
    return Settings.model_validate(_read_yaml(path))


def load_mapping(path: Path) -> MappingConfig:
    return MappingConfig.model_validate(_read_yaml(path))
