import os

import pkg_resources
from setuptools import setup

setup(
    name="whisper_bench",
    version="1.0.0",
    packages=["bench"],
    python_requires=">=3.7",
    install_requires=[
        str(r)
        for r in pkg_resources.parse_requirements(
            open(os.path.join(os.path.dirname(__file__), "requirements.txt"))
        )
    ],
    url="https://github.com/MayNiklas/whisper-bench",
    license="",
    author="MayNiklas",
    author_email="",
    description="",
    entry_points={
        "console_scripts": ["whisper_bench=bench.bench:cli"],
    },
)
