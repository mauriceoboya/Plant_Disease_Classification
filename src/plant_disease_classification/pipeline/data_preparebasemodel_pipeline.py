from plant_disease_classification.config.configuration import ConfigurationManager
from plant_disease_classification.components.data_preparebase_model import (
    PrepareBaseModel,
)
from plant_disease_classification import logger

STAGE2 = "Prepare Base Model"


class PrepareBaseModelPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            config = ConfigurationManager()
            prepare_base_model_config = config.get_prepare_model_config()
            prepare_base_model = PrepareBaseModel(config=prepare_base_model_config)
            prepare_base_model.get_base_model()
            prepare_base_model.update_base_model()
        except Exception as e:
            raise e


if __name__ == "__main__":
    try:
        logger.info(f"Starting >>>>>>>>{STAGE2} pipeline <<<<<<<<<<")
        pipeline = PrepareBaseModelPipeline()
        pipeline.main()
        logger.info(f"Completed >>>>>>>>{STAGE2} pipeline <<<<<<<<<<")
        logger.info("Prepare Base Model pipeline completed successfully.")
    except:
        logger.error("Prepare Base Model pipeline failed.")
