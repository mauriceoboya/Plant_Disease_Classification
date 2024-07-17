from plant_disease_classification.config.configuration import ConfigurationManager
from plant_disease_classification.components.model_callbacks import PrepareCallbacks
from plant_disease_classification import logger
STAGE3="Prepare Callbacks"


class ModelCallbacksPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            config=ConfigurationManager()
            prepare_callbacks_config=config.get_prepare_callbacks_config()
            prepare_callbacks=PrepareCallbacks(config=prepare_callbacks_config)
            callbacks_list=prepare_callbacks.get_tb_ckpt_callbacks()
        except Exception as e:
            print(e)


if __name__=="__main__":
    try:
        logger.info(f"Starting >>>>>>>>{STAGE3} pipeline <<<<<<<<<<")
        pipeline = ModelCallbacksPipeline()
        pipeline.main()
        logger.info(f"Completed >>>>>>>>{STAGE3} pipeline <<<<<<<<<<")
        logger.info("Model callbacks pipeline completed successfully.")
    except:
        logger.error("Model callbacks pipeline failed.")