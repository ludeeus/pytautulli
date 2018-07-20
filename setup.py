"""
Setup configuration
"""
import setuptools
import pytautulli

VERSION = pytautulli.__version__

with open("README.md", "r") as fh:
    LONG = fh.read()
setuptools.setup(
    name="pytautulli",
    version=VERSION,
    author="Joakim Sorensen",
    author_email="joasoe@gmail.com",
    description="",
    long_description=LONG,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/ludeeus/pytautulli",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
