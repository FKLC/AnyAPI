import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="anyapi",
    version="1.1.501",
    description="An API Wrapper For Every API",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/FKLC/AnyAPI",
    author="Fatih Kılıç",
    author_email="***REMOVED***",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["anyapi"],
    install_requires=["requests"],
)
