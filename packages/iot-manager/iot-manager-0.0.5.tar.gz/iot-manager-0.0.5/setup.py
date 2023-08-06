from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="iot-manager",
    version="0.0.5",
    packages=["iot-manager"],
    scripts=[],

    author="Dylan Crockett",
    author_email="dylanrcrockett@gmail.com",
    description="A management API for connecting and managing IoT Clients.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dylancrockett/iot-manager",
    project_urls={
        "Documentation": "https://iotmanager.readthedocs.io/",
        "Source Code": "https://github.com/dylancrockett/iot-manager"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires='>=3.6'
)
