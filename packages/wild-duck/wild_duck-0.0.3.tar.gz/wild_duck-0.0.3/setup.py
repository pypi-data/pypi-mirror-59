import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wild_duck",
    version="0.0.3",
    author="Ken Spencer",
    author_email="me@iotaspencer.me",
    description="""An API client to interface with the wildduck
     webmail application API.""",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IotaSpencer/wild_duck-py",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "wildduck=wildduck:main",
        ],
    },
)
