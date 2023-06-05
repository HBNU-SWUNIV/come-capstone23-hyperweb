from django.urls import path, include
from .views import Food_view
from . import views


urlpatterns = [
    path('Food_view', Food_view.as_view(), name='Food_view'),
]

