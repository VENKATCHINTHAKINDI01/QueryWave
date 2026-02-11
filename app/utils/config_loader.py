import yaml
from pathlib import Path
from typing import Any, Dict

from app.exceptions import RAGBaseException


class ConfigLoader:

    def __init__(self, config_dir: str = "configs"):
        self.config_dir = Path(config_dir)
        if not self.config_dir.exists():
            raise RAGBaseException(
                message=f"Config directory not found: {self.config_dir}",
                error_code="CONFIG_DIR_MISSING"
            )

    def load(self, filename: str) -> Dict[str, Any]:
        config_path = self.config_dir / filename
        
        if not config_path.exists():
            raise RAGBaseException(
                message=f"Config file not found: {filename}",
                error_code="CONFIG_FILE_MISSING"
            )
        try:
            with open(config_path, "r") as file:
                return yaml.safe_load(file) or {}
        except yaml.YAMLError as e:
            raise RAGBaseException(
                message=f"Invalid YAML format in {filename}",
                error_code="CONFIG_YAML_ERROR"
            ) from e
