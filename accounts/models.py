from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now


class Users(AbstractUser):

    matricula = models.IntegerField(unique=True)
    dt_troca_senha = models.DateField(default= now)
    def str(self):
        return self.username
    
    def save(self, *args, **kwargs):
        if not self.matricula:
            ultima_matricula = Users.objects.last().matricula if Users.objects.last() else 0

            self.matricula = ultima_matricula + 1
        super(Users, self).save(*args, **kwargs)    

    class Meta:
        db_table = 'usuario' #Define o nome da tabela
        verbose_name = 'Usuário' 
        verbose_name_plural = 'Usuários'


class Token(models.Model):
    codToken = models.CharField(max_length=6)
    usuario = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    datGer = models.DateField(auto_now_add=True)
    horGer = models.TimeField(auto_now_add=True)        