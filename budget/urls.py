from django.urls import path
from . import views
from budget import views

urlpatterns = [
    path('', views.index),
]