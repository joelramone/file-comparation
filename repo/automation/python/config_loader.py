from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import ValidationError

from .exceptions import ConfigurationError
from .models import MappingConfig, Settings


def _load_yaml(path: Path) -> dict:
    if not path.exists():
        raise ConfigurationError(f"Missing configuration file: {path}")
    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    if not isinstance(data, dict):
        raise ConfigurationError(f"Invalid YAML object in {path}")
    return data


def load_settings(path: Path) -> Settings:
    try:
        return Settings.model_validate(_load_yaml(path))
    except ValidationError as exc:
        raise ConfigurationError(f"Invalid settings: {exc}") from exc


def load_mappings(path: Path) -> MappingConfig:
    try:
        return MappingConfig.model_validate(_load_yaml(path))
    except ValidationError as exc:
        raise ConfigurationError(f"Invalid mapping: {exc}") from exc
