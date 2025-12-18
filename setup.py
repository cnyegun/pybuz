from setuptools import setup

setup(
    name="pybuz",
    version="0.1.0",
    author="Luke Nguyen",
    author_email="buichinguyen1105@gmail.com",
    description="Minimalistic python library for downloading high-quality music from Qobuz",
    url="https://github.com/cnyegun/pybuz",
    packages=["pybuz"],
    python_requires=">=3.10",
    install_requires=[
        "requests>=2.31.0",
    ],
)
