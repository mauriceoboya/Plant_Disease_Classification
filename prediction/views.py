from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import tensorflow as tf
import google.generativeai as genai
from tensorflow.keras.preprocessing import image
import numpy as np
import os
from pathlib import Path
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
from django_ratelimit.decorators import ratelimit


#@api_view(['POST'])
#@permission_classes([IsAuthenticated])
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
        base_dir = Path(__file__).resolve().parent
        model_path = base_dir / 'model.h5'
        model = tf.keras.models.load_model(model_path)

        # Preprocess the image
        try:
            processed_image = self.preprocess_image(file_path)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
 #      Make a prediction
        prediction = model.predict(processed_image)
        predicted_class = np.argmax(prediction, axis=-1)[0]

        # Map the predicted class to labels
        labels = {
            0: "Apple healthy", 1: "Apple leaf blotch", 2: "Apple rot", 3: "Apple rust", 4: "Apple scab",
            5: "Bell pepper bacterial spot", 6: "Bell pepper healthy", 7: "Blueberry healthy",
            8: "Cherry healthy", 9: "Corn common rust", 10: "Corn gray leaf spot", 11: "Corn northern leaf blight",
            12: "Grape black rot", 13: "Grape healthy", 14: "Peach healthy", 15: "Potato early blight", 16: "Potato early blight", 17: "Potato late blight",
            18: "Rice bacterial blight", 19: "Rice brown spot", 20: "Rice leaf smut", 21: "Soybean healthy",
            22: "Squash powdery mildew", 23: "Strawberry healthy", 24: "Tomato bacterial spot", 25: "Tomato early blight", 26: "Tomato healthy",
            27: "Tomato late blight", 28: "Tomato leaf curl", 29: "Tomato leaf mold", 30: "Tomato mosaic virus",
            31: "Tomato septoria leaf spot", 32: "Tomato spider mites"
        }

        predicted_label = labels.get(predicted_class)

        # Delete the image file after prediction
        default_storage.delete(file_path)

        # Generate prevention advice using Gemini API
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(f"how do i prevent {predicted_label}")

        return Response({
            'predicted_class': predicted_label,
            'prevention_advice': response.text
        }, status=status.HTTP_200_OK)
 
