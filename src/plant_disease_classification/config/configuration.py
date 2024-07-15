
from plant_disease_classification.entity.config_entity import DataIngestionConfig
from plant_disease_classification.utils.common import read_yaml, create_directories
from plant_disease_classification.constants import *

class ConfigurationManager:
    def __init__ (self,config=CONFIGURATION_FILE_PATH,params=PARAMS_FILE_PATH):
        self.config = read_yaml(config)
        self.params=read_yaml(params)

        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self)->DataIngestionConfig:
        config=self.config.data_ingestion
        create_directories([config.root_dir])

        data_ingestion_config=DataIngestionConfig(
            roo_dir=config.root_dir,
            source_URL=config.source_URL,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir
        )
        return data_ingestion_config
