import os
from typing import Optional


def get_env(key: str) -> Optional[str]:
    value = os.getenv(key)
    if value is None:
        raise EnvironmentError(f"Environment variable '{key}' not found")
    if value == "None":
        return None
    return value
