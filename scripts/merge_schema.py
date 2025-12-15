#!/usr/bin/env python3

import yaml
from pathlib import Path
from typing import Any


CORE = Path("schemas/core.schema.yaml")
USER = Path("schemas/user.schema.yaml")
OUT = Path("schemas/effective.schema.yaml")


def load_yaml(path: Path) -> dict[Any, Any]:
    if not Path(path).exists():
        return {}
    with path.open() as f:
        return yaml.safe_load(f) or {}
    

def merge_lists(core_list: list[Any] | None, user_list: list[Any] | None) -> list[Any]:
    if core_list is None:
        core_list = []
    if user_list is None:
        user_list = []
    return sorted(list(dict.fromkeys(core_list + user_list)))


def main():
    core = load_yaml(CORE)
    user = load_yaml(USER)

    merged = {
        "entity_types": merge_lists(core.get("entity_types"), user.get("entity_types"))
    }

    with OUT.open("w") as f:
        yaml.dump(merged, f, sort_keys=False, default_flow_style=False, indent=2)
    
    print(f'[OK] Schema merged successfully -> {OUT.__str__()}')


if __name__ == "__main__":
    main()