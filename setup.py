from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mredu",
    version="1.0.1",
    url="http://github.com/ramonpin/mredu",
    author="ramonpin",
    author_email="ramon.pin@gmail.com",
    description="A simple simulator of a system which implements map/reduce paradigm.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache-2",
    packages=["mredu"],
    install_requires=[
        "toolz>=0.12.0",
        "rich",
    ],
    zip_safe=False,
)
