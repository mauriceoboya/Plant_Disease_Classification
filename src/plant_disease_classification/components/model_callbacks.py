import tensorflow as tf
from plant_disease_classification.entity.config_entity import PrepareCallbacksConfig
import time
import os

class PrepareCallbacks:
    def __init__(self,config:PrepareCallbacksConfig):
        self.config=config
    
    @property
    def _create_tb_callbacks(self):
        timestamp=time.strftime("%Y-%m-%d-%H-%M-%S")
        tb_running_dir=os.path.join(
            self.config.tensorboard_root_log_dir,
            f"tb_logs_at_{timestamp}",      
        )
        return tf.keras.callbacks.TensorBoard(log_dir=tb_running_dir)
    
    @property
    def _create_ckpt_callbacks(self):
        return tf.keras.callbacks.ModelCheckpoint(
            filepath=self.config.checkpoint_model_filepath,
            save_weights_only=True,
            save_best_only=True
        )
    def get_tb_ckpt_callbacks(self):
        return [
            self._create_tb_callbacks,
            self._create_ckpt_callbacks
        ]
