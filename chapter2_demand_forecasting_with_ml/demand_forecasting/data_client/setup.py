import sys

from setuptools import setup

with open("README.md", encoding="utf-8") as readme_file:
    readme = readme_file.read()


def _requires_from_file(filename):
    return open(filename).read().splitlines()


info = sys.version_info

setup(
    name="data_client",
    version="0.0.0",
    description="data client",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="data_client",
    author_email="",
    url="https://github.com/shibuiwilliam/building-ml-system/tree/develop/chapter2_demand_forecasting_with_ml/demand_forecasting",
    packages=["data_client"],
    include_package_data=True,
    zip_safe=False,
    install_requires=_requires_from_file("./requirements.txt"),
    keywords="data_client",
    python_requires=">=3.9.5",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "Natural Language :: English",
        "Natural Language :: Japanese",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
)
