from django.urls import path, include
from . import auth_views

urlpatterns = [
    path('', include(auth_views)),
]
