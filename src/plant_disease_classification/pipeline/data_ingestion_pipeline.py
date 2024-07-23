from plant_disease_classification import logger
from plant_disease_classification.config.configuration import ConfigurationManager
from plant_disease_classification.components.data_ingestion import DataIngestion


STAGE1 = "Data ingestion"


class DataIngestionPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            config_manager = ConfigurationManager()
            data_ingestion_config = config_manager.get_data_ingestion_config()
            data_ingestion = DataIngestion(data_ingestion_config)
            data_ingestion.download_data()
            data_ingestion.extract_zip_file()

        except Exception as e:
            logger.error(f"Error in data ingestion: {str(e)}")


if __name__ == "__main__":
    try:
        logger.info(f"Starting >>>>>>>>{STAGE1} pipeline <<<<<<<<<<")
        pipeline = DataIngestionPipeline()
        pipeline.main()
        logger.info(f"Completed >>>>>>>>{STAGE1} pipeline <<<<<<<<<<")
        logger.info("Data ingestion pipeline completed successfully.")
    except:
        logger.error("An error occurred during the data ingestion pipeline execution.")
        logger.info("Data ingestion pipeline failed.")
