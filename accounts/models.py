from operator import mod
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from home.models import Escala, Endereco


class Users(AbstractUser):

    matricula = models.IntegerField(unique=True)
    dt_troca_senha = models.DateField(default= now)
    foto = models.ImageField(upload_to='imagens/usuario_img/%Y/%m/%d', blank=True, null=True)
    email = models.EmailField(unique=True, blank=False, null=False)
    escala = models.ForeignKey(Escala, on_delete=models.DO_NOTHING, blank=True, null=True)
    cargo = models.ForeignKey('Cargo', on_delete=models.DO_NOTHING, blank=True, null=True)
    justificar = models.BooleanField(blank=True, null=True, default=False)
    hora_extra = models.BooleanField(blank=True, null=True, default=False)
    dat_admissao = models.DateField(blank=True, null=True)
    dat_inicia_trab = models.DateField(blank=True, null=True)
    superior = models.ForeignKey('Users', on_delete=models.DO_NOTHING, blank=True, null=True)
    endereco = models.ForeignKey(Endereco, on_delete=models.DO_NOTHING, blank=True, null=True)


    def __str__(self):
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
    codToken = models.CharField(max_length=255)
    usuario = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    datGer = models.DateField(auto_now_add=True)
    horGer = models.TimeField(auto_now_add=True)        



class Cargo(models.Model):
    nmCargo = models.CharField(max_length=100)
    sitCargo = models.BooleanField()
    
    def __str__(self):
        return self.nmCargo

    class Meta:
        db_table = 'cargo'
        verbose_name = 'Cargo' 
        verbose_name_plural = 'Cargos'