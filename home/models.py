from pyexpat import model
from django.db import models
# from accounts.models import Users


class Escala(models.Model):
    nmEscala = models.CharField(max_length=90)
    horEnt1 = models.TimeField(blank=True, null=True)      
    horSai2 = models.TimeField(blank=True, null=True)      
    horEnt3 = models.TimeField(blank=True, null=True)      
    horSai4 = models.TimeField(blank=True, null=True) 
    segunda = models.BooleanField()
    terca = models.BooleanField()
    quarta = models.BooleanField()
    quinta = models.BooleanField()
    sexta = models.BooleanField()
    sabado = models.BooleanField()
    domingo = models.BooleanField()
    status = models.BooleanField()

    def __str__(self):
        return self.nmEscala

    class Meta:
       db_table = 'escala' #Define o nome da tabela
       verbose_name = 'Escala' 
       verbose_name_plural = 'Escalas'

class HoraExtra(models.Model):
    userExtra = models.ForeignKey('accounts.Users', on_delete=models.DO_NOTHING, related_name='userExtra')
    dataExtra = models.DateField(blank=True, null=True)
    userLib = models.ForeignKey('accounts.Users', on_delete=models.DO_NOTHING, blank=True, null=True, related_name='userLib')  
    dataLib = models.DateField(blank=True, null=True)
    horEnt1 = models.TimeField(blank=True, null=True)
    horSai2 = models.TimeField(blank=True, null=True)
    horEnt3 = models.TimeField(blank=True, null=True)
    horSai4 = models.TimeField(blank=True, null=True)
    sitApr = models.BooleanField(blank=True, null=True)

    class Meta:
       db_table = 'horaextra'
       verbose_name = 'Hora Extra' 
       verbose_name_plural = 'Horas Extras'

class HistRegistro(models.Model):
    userReg = models.ForeignKey('accounts.Users', on_delete=models.DO_NOTHING)
    escala = models.ForeignKey(Escala, on_delete=models.DO_NOTHING, blank=True, null=True)
    dataReg = models.DateField(blank=True, null=True)
    horEnt1 = models.TimeField(blank=True, null=True) 
    altEnt1 = models.BooleanField(blank=True, null=True, default=False)    
    horSai2 = models.TimeField(blank=True, null=True) 
    altSai2 = models.BooleanField(blank=True, null=True, default=False)     
    horEnt3 = models.TimeField(blank=True, null=True) 
    altEnt3 = models.BooleanField(blank=True, null=True, default=False)         
    horSai4 = models.TimeField(blank=True, null=True) 
    altSai4 = models.BooleanField(blank=True, null=True, default=False) 
    bancoHoraMin = models.IntegerField(blank=True, null=True, default=0)
    sitAPR =  models.CharField(max_length= 3, default='PEN') #PEN = Pendente, APR = Aprovado, REJ = Rejeitado
    # Verificar
    justificativas = models.ManyToManyField('home.Justificativa', blank=True)


    class Meta:
       db_table = 'histregistro'
       verbose_name = 'Histórico de Registro' 
       verbose_name_plural = 'Histórico de Registros'


class TipoJustificativa(models.Model):
    tipoJustificativa = models.CharField(max_length= 70)
    sitJust = models.BooleanField()
    
    def __str__(self):
        return self.tipoJustificativa

    class Meta:
       db_table = 'tipojustificativa'
       verbose_name = 'Tipo de Justificativa' 
       verbose_name_plural = 'Tipos de Justificativas'

class Justificativa(models.Model):
    txtJust = models.TextField()
    tipoJust = models.ForeignKey(TipoJustificativa, on_delete=models.DO_NOTHING)
    # histRegistro = models.ForeignKey('home.HistRegistro', models.CASCADE, related_name='Justificativa') #models.ForeignKey('home.HistRegistro', on_delete=models.DO_NOTHING)
    data = models.DateField()
    hora = models.TimeField()
    userReg = models.ForeignKey('accounts.Users', on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return self.txtJust

    class Meta:
       db_table = 'justificativa'
       verbose_name = 'Justificativa'
       verbose_name_plural = 'Justificativas'