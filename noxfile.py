"""Python module with nox sessions"""
import os
import re
from glob import glob
from pathlib import Path
from typing import Iterator

import nox


nox.options.error_on_missing_interpreters = True

HERE = Path(__file__).parent.absolute()

BANDIT_CONFIGURATION = str(HERE / "configs" / "bandit.yml")
GLOBAL_CONFIGURATION = str(HERE / "setup.cfg")

ADDITIONAL_FILES = [str(HERE / "noxfile.py")]

DEFAULT_PYTHON_INTERPRETER = "3.7"


def locate_linted_files() -> Iterator[str]:
    excluded = ["setup.py", "noxfile.py"]
    forbidden_re = re.compile(r"(venv|\.env|\.nox|\.venv)")
    return (
        file_path
        for file_path in glob("./**/*.py", recursive=True)
        if os.path.basename(file_path) not in excluded and not forbidden_re.search(file_path)
    )


@nox.session(python=DEFAULT_PYTHON_INTERPRETER)
def flake8(session: "nox.Session") -> None:
    flake8_plugins = (
        "flake8-bugbear",
        "flake8-colors",
        "flake8-docstrings",
        "flake8-typing-imports",
        "flake8-comprehensions",
        "flake8-eradicate",
        "flake8-annotations",
        "pep8-naming",
        "pycodestyle",
    )
    session.install("flake8", *flake8_plugins)
    session.run("flake8", ".")


@nox.session(python=DEFAULT_PYTHON_INTERPRETER)
def bandit(session: "nox.Session") -> None:
    session.install("bandit")
    session.run(
        "bandit", "-r", ".", "-c", BANDIT_CONFIGURATION,
    )


@nox.session(python=DEFAULT_PYTHON_INTERPRETER)
def mypy(session: "nox.Session") -> None:
    session.install("mypy")
    session.run("mypy", *locate_linted_files(), "--pretty", "--ignore-missing-imports")


@nox.session(python=False)
def kubeval(session: "nox.Session") -> None:
    k8s_folder = (HERE / "k8s").absolute()
    kubeval_image = "garethr/kubeval:0.15.0"
    session.run(
        "docker",
        "run",
        "--rm",
        "-v",
        f"{k8s_folder}:/usr/app/k8s",
        kubeval_image,
        "-d",
        "/usr/app/k8s/",
    )


@nox.session(python=DEFAULT_PYTHON_INTERPRETER)
def black(session: "nox.Session") -> None:
    session.install("black")
    session.run("black", "--line-length", "100", ".")


@nox.session(python=DEFAULT_PYTHON_INTERPRETER)
def isort(session: "nox.Session") -> None:
    session.install("isort")
    session.run(
        "isort",
        ".",
        "--settings-path",
        GLOBAL_CONFIGURATION,
        "--use-parentheses",
        "--trailing-comma",
        "--balanced",
        "--combine-as",
    )


@nox.session(python=DEFAULT_PYTHON_INTERPRETER)
def lint(session: "nox.Session") -> None:
    flake8(session)
    bandit(session)
    mypy(session)
    kubeval(session)


@nox.session(python=DEFAULT_PYTHON_INTERPRETER)
def reformat(session: "nox.Session") -> None:
    black(session)
    isort(session)
