from plant_disease_classification import logger
from plant_disease_classification.entity.config_entity import DataIngestionConfig
from kaggle.api.kaggle_api_extended import KaggleApi
import os
import zipfile


class DataIngestion:
    def __init__(self,config:DataIngestionConfig):
        self.config=config
        self.api = KaggleApi()
        self.api.authenticate()
    def download_data(self):
        try:
            dataset_id = self.config.source_URL
            zip_download_dir = os.path.dirname(self.config.local_data_file)  # Extract directory path
            os.makedirs(zip_download_dir, exist_ok=True)  # Ensure directory exists
            logger.info(f"Downloading data from {dataset_id} into directory {zip_download_dir}")
            self.api.dataset_download_files(dataset =dataset_id, path=zip_download_dir, unzip=False)
            logger.info(f"Downloaded data from {dataset_id} into directory {zip_download_dir}")
        except Exception as e:
            logger.error(f"Error downloading data from {dataset_id} into directory {zip_download_dir}")
            raise e


    def extract_zip_file(self):
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(self.config.unzip_dir)
        logger.info(f"Data extracted successfully to: {self.config.unzip_dir}")