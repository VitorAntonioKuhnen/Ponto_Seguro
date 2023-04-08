from django.db import models
# from accounts.models import Users


class Escala(models.Model):
    nmEscala = models.CharField(max_length=90)
    horaEntM = models.TimeField(blank=True, null=True)      
    horaSaiM = models.TimeField(blank=True, null=True)      
    horaEntV = models.TimeField(blank=True, null=True)      
    horaSaiV = models.TimeField(blank=True, null=True) 
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

class HistRegistro(models.Model):
    userReg = models.ForeignKey('accounts.Users', on_delete=models.DO_NOTHING)
    escala = models.ForeignKey(Escala, on_delete=models.DO_NOTHING, blank=True, null=True)
    dataReg = models.DateField(blank=True, null=True)
    horaEntM = models.TimeField(blank=True, null=True)      
    horaSaiM = models.TimeField(blank=True, null=True)      
    horaEntV = models.TimeField(blank=True, null=True)      
    horaSaiV = models.TimeField(blank=True, null=True)  
    bancoHora = models.TimeField(blank=True, null=True)
    sitAPR = models.BooleanField()

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
    tipoJust = models.ForeignKey(TipoJustificativa, on_delete=models.DO_NOTHING)
    data = models.DateField()
    hora = models.TimeField()
    userReg = models.ForeignKey('accounts.Users', on_delete=models.DO_NOTHING)

    class Meta:
       db_table = 'justificativa'
       verbose_name = 'Justificativa'
       verbose_name_plural = 'Justificativas'