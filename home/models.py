from django.db import models
# from accounts.models import Users


class Escala(models.Model):
    horaEntM = models.TimeField()      
    horaSaiM = models.TimeField()      
    horaEntV = models.TimeField()      
    horaSaiM = models.TimeField() 
    status = models.BooleanField()

    class Meta:
       db_table = 'escala' #Define o nome da tabela
       verbose_name = 'Escala' 
       verbose_name_plural = 'Escalas'

class HistRegistro(models.Model):
    userReg = models.ForeignKey('accounts.Users', on_delete=models.DO_NOTHING)
    dataReg = models.DateField()
    horaEntM = models.TimeField()      
    horaSaiM = models.TimeField()      
    horaEntV = models.TimeField()      
    horaSaiM = models.TimeField()  
    bancoHora = models.TimeField()
    sitReg = models.BooleanField()

    class Meta:
       db_table = 'histregistro'
       verbose_name = 'Histórico de Registro' 
       verbose_name_plural = 'Histórico de Registros'


class TipoJustificativa(models.Model):
    tipoJustificativa = models.CharField(max_length= 70)
    sitJust = models.BooleanField()

    class Meta:
       db_table = 'tipojustificativa'
       verbose_name = 'Tipo de Justificativa' 
       verbose_name_plural = 'Tipos de Justificativas'

class Justificativa(models.Model):
    tipoJust = models.ForeignKey(TipoJustificativa, on_delete=models.DO_NOTHING)
    data = models.DateField()
    hora = models.TimeField()
    userReg = models.ForeignKey('accounts.Users', on_delete=models.DO_NOTHING)

    class Meta:
       db_table = 'justificativa'
       verbose_name = 'Justificativa'
       verbose_name_plural = 'Justificativas'