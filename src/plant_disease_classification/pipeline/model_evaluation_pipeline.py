from plant_disease_classification import logger
from plant_disease_classification.config.configuration import ConfigurationManager
from plant_disease_classification.components.model_evaluation import Evaluation

STAGE5 = "Model Evaluation"


class ModelEvaluationPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            config_manager = ConfigurationManager()
            eval_config = config_manager.get_validation_config()
            evaluation = Evaluation(eval_config)
            evaluation.evaluation()
            evaluation.save_score()
        except Exception as e:
            logger.error(f"Error in validation: {str(e)}")


if __name__ == "__main__":
    try:
        logger.info(f"Starting >>>>>>>>{STAGE5} pipeline <<<<<<<<<<")
        pipeline = ModelEvaluationPipeline()
        pipeline.main()
        logger.info(f"Completed >>>>>>>>{STAGE5} pipeline <<<<<<<<<<")
        logger.info("Model Evaluation pipeline completed successfully.")
    except:
        logger.error("Model Evaluation pipeline failed.")
