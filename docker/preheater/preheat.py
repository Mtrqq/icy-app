from icy.classifier import list_available_models
from icy.classifier.recognize import _load_model  # noqa


def main():
    for model_name in map(str.lower, list_available_models()):
        _load_model(model_name, pretrained=True)  # noqa


if __name__ == "__main__":
    main()
