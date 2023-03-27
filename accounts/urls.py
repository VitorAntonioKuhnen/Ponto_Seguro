from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login, name='login'),
    path('validacao/', views.validacao, name='validacao'),
    path('token/<int:id>/', views.token, name='token'),
    path('gerarToken/<int:id>/', views.gerarToken, name='gerarToken'),
    # path('logout/', views.logout, name='logout'),
]
