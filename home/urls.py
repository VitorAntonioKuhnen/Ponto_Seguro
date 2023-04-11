from django.urls import path
from . import views

app = 'home'

urlpatterns = [
    path('RegistrarPonto/', views.RegistrarPonto, name='RegistrarPonto'),
]