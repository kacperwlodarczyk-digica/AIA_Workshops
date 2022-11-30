#!/usr/bin/env python3.9

from pathlib import Path
from setuptools import find_namespace_packages, setup


REQUIREMENTS_PATH = Path(__file__).parent / "requirements.txt"


def read_reqs(file_path: Path) -> list[str]:
    try:
        with open(file_path, "r") as f:
            return f.read().splitlines()
    except FileNotFoundError:
        print("File not found. Requirements default to an empty list.")
        return [""]


if __name__ == "__main__":
    setup(
        name="AIA_Workshops",
        version="0.0.0",
        packages=find_namespace_packages(exclude=("data",)),
        install_requires=read_reqs(REQUIREMENTS_PATH),
    )
