from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login, name='login'),
    path('validacao/', views.validacao, name='validacao'),
    path('enviaEmail/', views.enviaEmail, name='enviaEmail'),
    # path('logout/', views.logout, name='logout'),
]
