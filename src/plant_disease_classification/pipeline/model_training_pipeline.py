from plant_disease_classification.config.configuration import ConfigurationManager
from plant_disease_classification.components.model_callbacks import PrepareCallbacks
from plant_disease_classification.components.model_training import Training
from plant_disease_classification import logger


STAGE4='Model training'


class ModelTrainingPipeline:
    def __init__(self):
        pass
    def main(self):
                
        try:
            config=ConfigurationManager()
            prepare_callbacks_config=config.get_prepare_callbacks_config()
            prepare_callbacks=PrepareCallbacks(config=prepare_callbacks_config)
            callbacks_list=prepare_callbacks.get_tb_ckpt_callbacks()

            training_config=config.get_training_config()
            training=Training(config=training_config)
            training.get_base_model()
            training.train_valid_generator()
            training.train(callback_list=callbacks_list)

        except Exception as e:
            print(e)


try:
    logger.info(f"Starting >>>>>>>>{STAGE4} pipeline <<<<<<<<<<")
    pipeline = ModelTrainingPipeline()
    pipeline.main()
    logger.info(f"Completed >>>>>>>>{STAGE4} pipeline <<<<<<<<<<")
except:
    logger.error(f"An error occurred during the {STAGE4} pipeline execution.")