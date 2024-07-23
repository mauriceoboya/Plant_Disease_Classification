from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import os

class PredictImageView(APIView):

    def preprocess_image(self, image_path):
        img = image.load_img(image_path, target_size=(224, 224))  # Adjust target_size
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)  # Create batch axis
        img_array = img_array / 255.0  # Normalize to [0,1]
        return img_array

    def post(self, request, *args, **kwargs):
        # Save the uploaded image
        file = request.FILES['image']
        file_name = default_storage.save(file.name, ContentFile(file.read()))
        file_path = os.path.join(default_storage.location, file_name)

        # Load the model
        model = tf.keras.models.load_model("artifacts/training/model.h5")

        # Preprocess the image
        try:
            processed_image = self.preprocess_image(file_path)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Make a prediction
        prediction = model.predict(processed_image)
        predicted_class = np.argmax(prediction, axis=-1)[0]

        # Delete the image file after prediction
        default_storage.delete(file_path)

        return Response({'predicted_class': int(predicted_class)}, status=status.HTTP_200_OK)
