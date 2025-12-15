#!/usr/bin/env python3

import yaml
import sys
from pathlib import Path
from typing import Any, TypeGuard


def load_yaml(path: str) -> dict[Any, Any]:
    if not Path(path).exists():
        return {}
    with open(path, 'r') as f:
        return yaml.safe_load(f) or {}
    

def validate_list(name: str, data_list: TypeGuard[list[Any]] | None):
    if data_list is None:
        raise ValueError(f'{name} must be present and be a list.')
    if not isinstance(data_list, list):
        raise ValueError(f'{name} must be a list.')
    if len(data_list) == 0:
        raise ValueError(f'{name} cannot be empty.')
    if len(data_list) != len(set(data_list)): # pyright: ignore[reportUnknownArgumentType]
        raise ValueError(f'{name} contains duplicate entries.')
    

def validate_schema(schema: dict[Any, Any]):
    validate_list('entity_types', schema.get('entity_types'))

    for item in schema['entity_types']:
        if not isinstance(item, str) or item.strip() == "":
            raise ValueError(f'Invalid entity type: {item}')
        

def main(schema_path: str):
    if not Path(schema_path).exists():
        print(f'Schema not found: {schema_path}')
        sys.exit(1)
    
    schema = load_yaml(schema_path)

    try:
        validate_schema(schema=schema)
        print(f'[OK] Schema validation passed.')
    except Exception as e:
        print(f'[ERROR] Schema validation failed: {e}')
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: validate_schema.py <effective.yaml>")
        sys.exit(1)
    main(sys.argv[1])