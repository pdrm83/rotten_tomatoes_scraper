import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="rotten_tomatoes_scraper",
    version="1.3.1",
    description="How to scrape Rotten Tomatoes website using an easy interface.",
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
    install_requires=['bs4', 'requests', 'lxml'],
    entry_points={
        "console_scripts": [
            "pdrm83=rotten_tomatoes_scraper.__main__:main",
        ]
    },
)