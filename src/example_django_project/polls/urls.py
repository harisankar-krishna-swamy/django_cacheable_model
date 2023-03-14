from django.urls import path

from .views import Choices, Questions

urlpatterns = [
    path('choices/', Choices.as_view(), name='choices'),
    path('questions/', Questions.as_view(), name='questions'),
]
