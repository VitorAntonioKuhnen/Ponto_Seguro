from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('RegistrarPonto/', views.RegistrarPonto, name='RegistrarPonto'),
    path('mostrahtml/', views.mostrahtml, name='mostrahtml'),
    path('historico/', views.historico, name='historico'),
    path('aprovaPonto/', views.aprovaPonto, name='aprovaPonto'),
    path('aprovar/<int:id>/', views.aprovar, name='aprovar'),
    path('desaprovar/<int:id>/', views.desaprovar, name='desaprovar'),
    path('altRegistro/<int:id>/', views.altRegistro, name='altRegistro'),
]