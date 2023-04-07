from django.urls import path
from . import views


urlpatterns = [
    path('RegistrarPonto/', views.RegistrarPonto, name='RegistrarPonto'),
]