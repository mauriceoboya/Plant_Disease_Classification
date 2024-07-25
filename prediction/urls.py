from django.urls import path
from .views import PredictImageView

urlpatterns = [
    path('predict/', PredictImageView.as_view(), name='predict'),
]