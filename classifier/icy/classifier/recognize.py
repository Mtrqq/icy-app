import logging
from itertools import takewhile
from typing import List, Tuple

import requests


_DEFAULT_MEAN: List[float] = [0.485, 0.456, 0.406]
_DEFAULT_STD: List[float] = [0.229, 0.224, 0.225]
_PROBABILITY_THRESHOLD: float = 0.005


logging.basicConfig(level="INFO", format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logger = logging.getLogger(__name__)


def load_image(image_url: str) -> "PIL.Image.Image":
    from PIL import Image

    logger.info("Loading image from url '%s'", image_url)
    get_response = requests.get(image_url, stream=True)
    if get_response.status_code != 200:
        raise ValueError("Invalid image url provided, unable to load image")
    return Image.open(get_response.raw).convert("RGB")


def _make_preprocessor(mean: List[float], std: List[float]) -> "transforms.Compose":
    import torchvision.transforms as transforms

    normalize = transforms.Normalize(mean=mean, std=std)
    return transforms.Compose(
        [transforms.Resize(256), transforms.CenterCrop(224), transforms.ToTensor(), normalize]
    )


def _load_model(model_name: str, pretrained: bool = True) -> "nn.Module":
    import torchvision.models as models

    try:
        loader = getattr(models, model_name)
        logger.info("Loading pretrained model (%s)", model_name)
        return loader(pretrained=pretrained)
    except AttributeError as error:
        raise RuntimeError(f"Unsupported model type '{model_name}'") from error


def _prepare_operators(model_name: str) -> Tuple["nn.Module", "nn.Softmax", "transforms.Compose"]:
    import torch.nn as nn

    model = _load_model(model_name=model_name)
    softmax = nn.Softmax(dim=1)
    preprocessor = _make_preprocessor(mean=_DEFAULT_MEAN, std=_DEFAULT_STD)
    return model, softmax, preprocessor


def recognize_image(image_url: str, model_name: str) -> List[Tuple[int, float]]:
    import torch.autograd as autograd

    image = load_image(image_url=image_url)
    model, softmax, preprocessor = _prepare_operators(model_name=model_name)
    inputs = preprocessor(image)
    inputs.unsqueeze_(0)  # unsqueeze inplace
    logger.info("Start processing image")
    classification_matrix = softmax(model(autograd.Variable(inputs)))[0].sort(descending=True)
    logger.info("Processing finished ! Preparing output data")
    values, indices = classification_matrix.values, classification_matrix.indices
    return [
        (int(label), float(prob))
        for label, prob in takewhile(lambda x: x[1] > _PROBABILITY_THRESHOLD, zip(indices, values))
    ]
