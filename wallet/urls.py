from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('add', views.add_record, name='add_record'),
    path('update/<int:id>', views.update_record, name='update_record'),
]
