"""
Utility functions for converting IDs between different formats
"""


def int_id_to_str(id_value: int) -> str:
    """
    Convert integer ID to string ID
    """
    return str(id_value)


def str_id_to_int(id_value: str) -> int:
    """
    Convert string ID to integer ID
    """
    try:
        return int(id_value)
    except ValueError:
        raise ValueError(f"Invalid ID format: {id_value} is not a valid integer")


def convert_ids_in_data(data: dict, convert_func) -> dict:
    """
    Convert IDs in a data dictionary using the provided conversion function
    """
    if 'id' in data:
        data['id'] = convert_func(data['id'])

    # Handle nested objects that might have IDs
    for key, value in data.items():
        if isinstance(value, dict) and 'id' in value:
            data[key]['id'] = convert_func(value['id'])
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict) and 'id' in item:
                    item['id'] = convert_func(item['id'])

    return data