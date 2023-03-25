from django.db import models
from django.contrib.auth.models import AbstractUser, User

class User(AbstractUser):

    matricula = models.CharField(max_length=10, unique=True)
    dt_troca_senha = models.DateField()
    def str(self):
        return self.username

    class Meta:
        db_table = 'usuario' #Define o nome da tabela
        verbose_name = 'Usuário' 
        verbose_name_plural = 'Usuários'