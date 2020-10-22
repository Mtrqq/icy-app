__all__ = ["list_available_models", "recognize_image", "stringify_label"]

from pathlib import Path
from typing import List, Tuple, Union

from icy.classifier.recognize import recognize_image as _recognize_image
from icy.classifier.utils import load_json_cached as _load_json


HERE = Path(__file__).parent
LABELS_MAPPING_FILE = HERE / "data" / "labels.json"
AVAILABLE_MODELS_FILE = HERE / "data" / "models.json"


def list_available_models() -> List[str]:
    return [model_name for model_name in _load_json(AVAILABLE_MODELS_FILE).keys()]


def recognize_image(
    image_url: str, model_name: str, stringify_labels: bool = False
) -> List[Union[Tuple[int, float], Tuple[str, float]]]:
    try:
        probability_mapping = _recognize_image(image_url=image_url, model_name=model_name.lower())
    except ImportError as error:
        raise RuntimeError("Core components of img-classifier were not installed") from error

    if stringify_labels:
        return [(stringify_label(label), prob) for label, prob in probability_mapping]
    return probability_mapping


def stringify_label(label: int) -> str:
    labels_mapping = _load_json(LABELS_MAPPING_FILE)
    return labels_mapping[str(label)]
