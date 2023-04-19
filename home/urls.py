from django.urls import path
from . import views

app = 'home'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('RegistrarPonto/', views.RegistrarPonto, name='RegistrarPonto'),
]