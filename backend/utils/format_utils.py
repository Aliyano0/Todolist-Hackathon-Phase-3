"""
Utility functions for formatting data between backend and frontend
"""

import re
from typing import Dict, Any, Union, List


def snake_to_camel(snake_str: str) -> str:
    """
    Convert snake_case string to camelCase
    """
    components = snake_str.split('_')
    return components[0] + ''.join(x.capitalize() for x in components[1:])


def camel_to_snake(camel_str: str) -> str:
    """
    Convert camelCase string to snake_case
    """
    s1 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', camel_str)
    return s1.lower()


def convert_dict_keys_to_camel(data: Union[Dict[str, Any], List, None]) -> Union[Dict[str, Any], List, None]:
    """
    Recursively convert dictionary keys from snake_case to camelCase
    """
    if data is None:
        return None
    elif isinstance(data, list):
        return [convert_dict_keys_to_camel(item) for item in data]
    elif isinstance(data, dict):
        converted = {}
        for key, value in data.items():
            camel_key = snake_to_camel(key)
            if isinstance(value, (dict, list)) and value is not None:
                converted[camel_key] = convert_dict_keys_to_camel(value)
            else:
                converted[camel_key] = value
        return converted
    else:
        return data


def convert_dict_keys_to_snake(data: Union[Dict[str, Any], List, None]) -> Union[Dict[str, Any], List, None]:
    """
    Recursively convert dictionary keys from camelCase to snake_case
    """
    if data is None:
        return None
    elif isinstance(data, list):
        return [convert_dict_keys_to_snake(item) for item in data]
    elif isinstance(data, dict):
        converted = {}
        for key, value in data.items():
            snake_key = camel_to_snake(key)
            if isinstance(value, (dict, list)) and value is not None:
                converted[snake_key] = convert_dict_keys_to_snake(value)
            else:
                converted[snake_key] = value
        return converted
    else:
        return data