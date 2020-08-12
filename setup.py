import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="rotten_tomatoes_scraper",
    version="1.0.1",
    description="How to extract movie genres from Rotten Tomatoes website",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/pdrm83/rotten_tomatoes_scraper",
    author="Pedram Ataee",
    author_email="pedram.ataee@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["rotten_tomatoes_scraper"],
    include_package_data=True,
    install_requires=['re', 'bs4', 'urllib', 'rotten_tomatoes_client'],
    entry_points={
        "console_scripts": [
            "pdrm83=rotten_tomatoes_scraper.__main__:main",
        ]
    },
)