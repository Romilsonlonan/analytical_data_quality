import os
from pathlib import Path
from functools import lru_cache
from typing import Any

import yaml


BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings:
    def __init__(self, env: str | None = None):
        self.env = env or os.getenv("APP_ENV", "dev")
        self._config: dict[str, Any] = self._load_config()

    def _load_config(self) -> dict[str, Any]:
        config_file = BASE_DIR / "config" / "environments" / f"{self.env}.yml"
        if not config_file.exists():
            raise FileNotFoundError(f"Config file not found: {config_file}")

        with open(config_file, "r") as f:
            config: dict[str, Any] = yaml.safe_load(f) or {}

        config = self._resolve_env_vars(config)
        return config

    def _resolve_env_vars(self, config: Any) -> Any:
        if isinstance(config, dict):
            return {k: self._resolve_env_vars(v) for k, v in config.items()}
        elif isinstance(config, list):
            return [self._resolve_env_vars(item) for item in config]
        elif isinstance(config, str) and config.startswith("${") and config.endswith("}"):
            env_var = config[2:-1]
            return os.getenv(env_var, config)
        return config

    @property
    def database(self) -> dict[str, Any]:
        return self._config.get("database", {})

    @property
    def minio(self) -> dict[str, Any]:
        return self._config.get("minio", {})

    @property
    def airflow(self) -> dict[str, Any]:
        return self._config.get("airflow", {})

    @property
    def dbt(self) -> dict[str, Any]:
        return self._config.get("dbt", {})

    @property
    def observability(self) -> dict[str, Any]:
        return self._config.get("observability", {})

    @property
    def features(self) -> dict[str, Any]:
        return self._config.get("features", {})

    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split(".")
        value: Any = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
