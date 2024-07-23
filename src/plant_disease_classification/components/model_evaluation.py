import tensorflow as tf
from pathlib import Path
from plant_disease_classification.entity.config_entity import EvaluationConfig
from plant_disease_classification.utils.common import save_json
from plant_disease_classification import logger
class Evaluation:
    def __init__(self, config: EvaluationConfig):
        self.config = config
    
    def _valid_generator(self):
        datagenerator_kwargs=dict(
            rescale=1./255,
            validation_split=0.30
        )
        dataflow_kwargs=dict(
            target_size=self.config.params_image_size,
            batch_size=self.config.params_batch_size,
            interpolation='bilinear'
        )
        valid_datagenerator=tf.keras.preprocessing.image.ImageDataGenerator(
            **datagenerator_kwargs
        )
        self.valid_generator=valid_datagenerator.flow_from_directory(
            directory=self.config.training_data,
            subset='validation',
            shuffle=False,
            **dataflow_kwargs
        )
    @staticmethod
    def load_model(path:Path)->tf.keras.Model:
        return tf.keras.models.load_model(path)
    
    def evaluation(self):
        model=self.load_model(self.config.path_of_model)
        self._valid_generator()
        self.score=model.evaluate(self.valid_generator)

    def save_score(self):
        if self.score is None:
            raise ValueError("No score to save. Please run evaluation first.")
        scores = {"loss": self.score[0], "accuracy": self.score[1]}
        logger.info('saving to json')
        save_json(path=Path('scores.json'), data=scores)