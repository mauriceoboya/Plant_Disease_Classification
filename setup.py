import setuptools
import os

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

REPO_NAME = "Plant_Disease_Classification"
SRC_REPO = f"plant_disease_classification"
version = "0.1.0"
email = "mauriq97@gmail.com"
author = "mauriceoboya"


setuptools.setup(
    name=SRC_REPO,
    version=version,
    author=author,
    author_email=email,
    long_description=long_description,
    url="https://github.com/{author}/{REPO_NAME}",
    project_urls={
        "Documentation": f"https://github.com/{author}/{REPO_NAME}/tree/master/docs",
        "Source Code": f"https://github.com/{author}/{REPO_NAME}",
        "Issue Tracker": f"https://github.com/{author}/{REPO_NAME}/issues",
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
