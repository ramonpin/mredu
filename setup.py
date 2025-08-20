from setuptools import setup

setup(
    name="mredu",
    version="1.0.0",
    description="A simple simulator of a system which implements map/reduce paradigm.",
    url="http://github.com/ramonpin/mredu",
    author="ramonpin",
    author_email="ramon.pin@gmail.com",
    license="Apache-2",
    packages=["mredu"],
    install_requires=[
        "toolz>=0.12.0",
        "rich",
    ],
    zip_safe=False,
)
