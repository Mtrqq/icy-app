import functools
import json
from pathlib import Path
from typing import Any, Union


@functools.lru_cache()
def load_json_cached(file_path: Union[str, Path]) -> Any:
    with open(file_path) as fp:
        return json.load(fp)
