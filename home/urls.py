from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('RegistrarPonto/', views.RegistrarPonto, name='RegistrarPonto'),
    path('mostrahtml/', views.mostrahtml, name='mostrahtml'),
    path('historico/', views.historico, name='historico'),
    path('aprovaPonto/', views.aprovaPonto, name='aprovaPonto'),
]