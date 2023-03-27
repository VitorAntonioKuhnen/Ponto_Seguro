from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.utils import timezone

class User(AbstractUser):

    matricula = models.CharField(max_length=10, unique=True)
    dt_troca_senha = models.DateField(timezone.now)
    def str(self):
        return self.username

    class Meta:
        db_table = 'usuario' #Define o nome da tabela
        verbose_name = 'Usuário' 
        verbose_name_plural = 'Usuários'


class Token(models.Model):
    codToken = models.CharField(max_length=6)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    datGer = models.DateField(auto_now_add=True)
    horGer = models.TimeField(auto_now_add=True)        