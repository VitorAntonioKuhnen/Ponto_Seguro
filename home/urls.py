from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('RegistrarPonto/', views.RegistrarPonto, name='RegistrarPonto'),
    path('historico/', views.historico, name='historico'),
    path('aprovaPonto/', views.aprovaPonto, name='aprovaPonto'),
    path('aprovaPontoHE/', views.aprovaPontoHE, name='aprovaPontoHE'),
    path('aprovar/<int:id>/', views.aprovar, name='aprovar'),
    path('desaprovar/<int:id>/', views.desaprovar, name='desaprovar'),
    path('aprovarHE/<int:id>/', views.aprovarHE, name='aprovarHE'),
    path('desaprovarHE/<int:id>/', views.desaprovarHE, name='desaprovarHE'),
    path('escala/', views.escala, name='escala'),
    path('cadastroEscala/', views.cadastroEscala, name='cadastroEscala'),
    path('alteraEscala/<int:id>/', views.alteraEscala, name='alteraEscala'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('altUsuario/<int:id>/', views.altUsuario, name='altUsuario'),
]