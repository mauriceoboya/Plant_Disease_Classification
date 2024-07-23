import logging
import os
from pathlib import Path


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s  %(message)s "
)

project = "plant_disease_classification"

list_of_files = [
    ".github/workflows/.gitkeep",
    "config/config.yaml",
    "params.yaml",
    "schema.yaml",
    "Dockerfile",
    "templates/index.html",
    "research/test.ipynb",
    "main.py",
    f"src/{project}/__init__.py",
    f"src/{project}/constants/__init__.py",
    f"src/{project}/config/configuration.py",
    f"src/{project}/utils/common.py",
    f"src/{project}/entity/config_entity.py",
    f"src/{project}/components/__init__.py",
    f"src/{project}/pipeline/__init__.py",
    "dvc.yaml",
    "setup.py",
]


for file in list_of_files:
    file = Path(file)
    file_dir = file.parent

    if file_dir != Path("."):
        try:
            if not file_dir.exists():
                file_dir.mkdir(parents=True, exist_ok=True)
                logging.info(f"Created directory: {file_dir}")
        except Exception as e:
            logging.error(f"Error creating directory: {file_dir}, error: {str(e)}")

    if not file.exists():
        try:
            file.touch()
            logging.info(f"Created file: {file}")
        except Exception as e:
            logging.error(f"Error creating file: {file}, error: {str(e)}")
    else:
        logging.info(f"File already exists: {file}")
