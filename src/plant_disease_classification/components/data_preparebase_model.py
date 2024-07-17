from plant_disease_classification import logger
from plant_disease_classification.entity.config_entity import PrepareBaseModelConfig
import tensorflow as tf
from pathlib import Path


class PrepareBaseModel:
    def __init__(self,config: PrepareBaseModelConfig):
        self.config=config

    def get_base_model(self):
        self.model=tf.keras.applications.VGG16(
            include_top=self.config.params_include_top,
            weights=self.config.params_weights,
            input_shape=self.config.params_image_size
        )
        self.save_model(path=self.config.base_model_path,model=self.model)
    @staticmethod
    def _prepare_full_model(model,classes,freeze_all,freeze_till,Learning_rate):
        if freeze_all:
            for layer in model.layers:
                layer.trainable = False
        elif (freeze_till is not None) and (freeze_all>0):
            for layer in model.layers[:-freeze_till]:
                layer.trainable = False
        flattin_in=tf.keras.layers.Flatten()(model.output)
        prediction=tf.keras.layers.Dense(
            classes,
            activation='softmax'
            )(flattin_in)
        full_model=tf.keras.models.Model(
            inputs=model.input,
            outputs=prediction
            )
        full_model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=Learning_rate),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        full_model.summary()
        return full_model
    
    def update_base_model(self):
        self.full_model=self._prepare_full_model(
            model=self.model,
            classes=self.config.params_classes,
            freeze_all=True,
            freeze_till=None,
            Learning_rate=self.config.params_learning_rate
        )
        self.save_model(path=self.config.updated_base_model_path,model=self.full_model)

    @staticmethod
    def save_model(path:Path, model:tf.keras.Model):
        model.save(path)
        logger.info(f"Model saved successfully at {path}")
        