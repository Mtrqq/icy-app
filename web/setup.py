from pathlib import Path
from typing import List

from setuptools import find_namespace_packages, setup


PACKAGE_NAME = "icy-server"
SUMMARY = "Web service for image classification"
CLASSIFIERS = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Natural Language :: English",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
]
AUTHOR = "Mtrqq"
COPYRIGHT = "Copyright 2020 {0}".format(AUTHOR)

HERE: Path = Path(__file__).parent
README: str = Path(HERE, "README.md").read_text(encoding="utf-8")
VERSION: str = Path(HERE, "VERSION").read_text()
REQUIREMENTS: List[str] = Path(HERE, "requirements.txt").read_text().splitlines()

if __name__ == "__main__":
    setup(
        name=PACKAGE_NAME,
        author=AUTHOR,
        description=SUMMARY,
        classifiers=CLASSIFIERS,
        version=VERSION,
        long_description=README,
        long_description_content_type="text/markdown",
        include_package_data=True,
        packages=find_namespace_packages(),
        install_requires=REQUIREMENTS,
    )
