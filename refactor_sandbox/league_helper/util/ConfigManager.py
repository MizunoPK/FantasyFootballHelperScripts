"""
Abstract base class for configuration managers.

Provides shared JSON reading and validation logic for all config managers.
"""

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict


class ConfigManager(ABC):
    """Abstract base class for all configuration managers."""

    def __init__(self, config_path : Path):
        """Initialize the config manager and load configuration."""
        self.config_name: str = ""
        self.description: str = ""
        self.parameters: Dict[str, Any] = {}
        self.config_path = config_path
        self._load_config()

    def _load_config(self) -> None:

        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

        with open(self.config_path, 'r') as f:
            data = json.load(f)

        # Validate required fields
        self._validate_config_structure(data)

        # Store configuration data
        self.config_name = data.get("config_name", "")
        self.description = data.get("description", "")
        self.parameters = data.get("parameters", {})

        # Allow child classes to perform additional validation/processing
        self._post_load_validation()

    def _validate_config_structure(self, data: Dict[str, Any]) -> None:
        """
        Validate that the configuration has the required structure.

        Args:
            data: The loaded JSON data

        Raises:
            ValueError: If required fields are missing
        """
        required_fields = ["config_name", "description", "parameters"]
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            raise ValueError(
                f"Configuration missing required fields: {', '.join(missing_fields)}"
            )

        if not isinstance(data["parameters"], dict):
            raise ValueError("'parameters' field must be a dictionary")

    def _post_load_validation(self) -> None:
        """
        Hook for child classes to perform additional validation after loading.

        Override this method in child classes to validate specific parameters.
        """
        pass

    def get_parameter(self, key: str, default: Any = None) -> Any:
        """
        Get a parameter value by key.

        Args:
            key: The parameter key
            default: Default value if key not found

        Returns:
            The parameter value or default
        """
        return self.parameters.get(key, default)

    def has_parameter(self, key: str) -> bool:
        """
        Check if a parameter exists.

        Args:
            key: The parameter key

        Returns:
            True if parameter exists, False otherwise
        """
        return key in self.parameters

    def __repr__(self) -> str:
        """String representation of the config manager."""
        return f"{self.__class__.__name__}(config_name='{self.config_name}')"
