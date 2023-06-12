from django.db import models
from datetime import datetime, time
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
    userAltHe = models.ForeignKey('accounts.Users', on_delete=models.DO_NOTHING, blank=True, null=True, related_name='userAltHe')  
    dataAlt = models.DateField(blank=True, null=True)
    horEnt1 = models.TimeField(blank=True, null=True)
    altEnt1 = models.BooleanField(blank=True, null=True, default=False)    
    horSai2 = models.TimeField(blank=True, null=True)
    altSai2 = models.BooleanField(blank=True, null=True, default=False) 
    horEnt3 = models.TimeField(blank=True, null=True)
    altEnt3 = models.BooleanField(blank=True, null=True, default=False) 
    horSai4 = models.TimeField(blank=True, null=True)
    altSai4 = models.BooleanField(blank=True, null=True, default=False)
    obsSup = models.TextField(blank=True, null=True)
    sitAPR = models.CharField(max_length= 3, default='PEN') #PEN = Pendente, APR = Aprovado, REJ = Rejeitado
    justificativas = models.ManyToManyField('home.Justificativa',  symmetrical=False)
    

    class Meta:
       db_table = 'horaextra'
       verbose_name = 'Hora Extra' 
       verbose_name_plural = 'Horas Extras'

    @property
    def diff_formatted(self):

        if (self.horEnt1 is not None) and (self.horSai2 is not None) and (self.horEnt3 is None) and (self.horSai4 is None):
            primeiroPeriod = datetime.combine(datetime.today(), self.horEnt1) - datetime.combine(datetime.today(), self.horSai2)
            hours = abs(primeiroPeriod.total_seconds()) // 3600
            minutes = (abs(primeiroPeriod.total_seconds()) % 3600) // 60
            return f"{int(hours):02d}:{int(minutes):02d}"  
        
        elif (self.horEnt1 is not None) and (self.horSai2 is not None) and (self.horEnt3 is not None) and (self.horSai4 is None):
            primeiroPeriod = datetime.combine(datetime.today(), self.horEnt1) - datetime.combine(datetime.today(), self.horSai2)
            hours = abs(primeiroPeriod.total_seconds()) // 3600
            minutes = (abs(primeiroPeriod.total_seconds()) % 3600) // 60
            return f"{int(hours):02d}:{int(minutes):02d}"  
        
        elif (self.horEnt1 is not None) and (self.horSai2 is not None) and (self.horEnt3 is not None) and (self.horSai4 is not None):
            primeiroPeriod = datetime.combine(datetime.today(), self.horEnt1) - datetime.combine(datetime.today(), self.horSai2)
            segundoPeriod = datetime.combine(datetime.today(), self.horEnt3) - datetime.combine(datetime.today(), self.horSai4)
            horExt = primeiroPeriod + segundoPeriod
            hours = abs(horExt.total_seconds()) // 3600
            minutes = (abs(horExt.total_seconds()) % 3600) // 60
            return f"{int(hours):02d}:{int(minutes):02d}"  
        else:
            return "00:00"  
    

class HistRegistro(models.Model):
    userReg = models.ForeignKey('accounts.Users', on_delete=models.DO_NOTHING)
    escala = models.ForeignKey(Escala, on_delete=models.DO_NOTHING, blank=True, null=True)
    dataReg = models.DateField(blank=True, null=True)
    userAlt = models.ForeignKey('accounts.Users', on_delete=models.DO_NOTHING, blank=True, null=True, related_name='userAlt')  
    dataAlt = models.DateField(blank=True, null=True)
    horEnt1 = models.TimeField(blank=True, null=True) 
    altEnt1 = models.BooleanField(blank=True, null=True, default=False)    
    horSai2 = models.TimeField(blank=True, null=True) 
    altSai2 = models.BooleanField(blank=True, null=True, default=False)     
    horEnt3 = models.TimeField(blank=True, null=True) 
    altEnt3 = models.BooleanField(blank=True, null=True, default=False)         
    horSai4 = models.TimeField(blank=True, null=True) 
    altSai4 = models.BooleanField(blank=True, null=True, default=False) 
    obsSup = models.TextField(blank=True, null=True) 
    #Processo inativado temporariamente
    # bancoHoraMin = models.IntegerField(blank=True, null=True, default=0)
    sitAPR =  models.CharField(max_length= 3, default='PEN') #PEN = Pendente, APR = Aprovado, REJ = Rejeitado
    justificativas = models.ManyToManyField('home.Justificativa',  symmetrical=False)


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


class Endereco(models.Model):
    logradouro = models.CharField(max_length=255)
    numero = models.CharField(max_length=255)
    complemento = models.CharField(max_length=255, blank=True, null=True)
    bairro = models.CharField(max_length=255)
    cidade = models.CharField(max_length=255)
    estado = models.CharField(max_length=255)
    cep = models.IntegerField()
    def __str__(self):
        return self.logradouro
        # return 'Logradouro: ' + self.logradouro + ' Nº: ' + self.numero + ' Bairro: ' + self.bairro + ' Cidade: ' + self.cidade + ' Estado: ' + self.estado  + ' CEP: ' + self.cep 

    class Meta:
       db_table = 'endereco'
       verbose_name = 'Endereco'
       verbose_name_plural = 'Enderecos'

class Tipo_Feriado(models.Model):
    nmTipo = models.CharField(max_length=255)

    def __str__(self):
        return self.nmTipo
    
    class Meta:
       db_table = 'tipo_feriado'
       verbose_name = 'Tipo_Feriado'
       verbose_name_plural = 'Tipos_de_Feriados'

class Level_Feriado(models.Model):
    nmLevel = models.CharField(max_length=255)
    endereco = models.ForeignKey(Endereco, on_delete=models.DO_NOTHING, blank=True, null=True)
    
    def __str__(self):
        return self.nmLevel
    
    class Meta:
       db_table = 'level_feriado'
       verbose_name = 'Level_Feriado'
       verbose_name_plural = 'Leveis_de_Feriados'

class Feriado(models.Model):
    data = models.DateField()
    nome = models.CharField(max_length=255)
    tipo = models.ForeignKey(Tipo_Feriado, on_delete=models.DO_NOTHING)
    level = models.ForeignKey(Level_Feriado, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nome
    
    class Meta:
       db_table = 'feriado'
       verbose_name = 'Feriado'
       verbose_name_plural = 'Feriados'
    