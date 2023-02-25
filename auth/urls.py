from django.urls import path
from . import views

urlpatterns = [
    path('login', views.auth_login, name='login user'),
    path('logout', views.auth_logout, name='logout user')
]