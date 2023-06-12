from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Escala, HistRegistro, Justificativa, TipoJustificativa, HoraExtra, Endereco, Feriado, Level_Feriado, Tipo_Feriado


class EscalaAdmin(admin.ModelAdmin):
    list_display = ['nmEscala', 'horEnt1', 'horSai2', 'horEnt3', 'horSai4', 'status']
    list_display_links = ['nmEscala', 'horEnt1', 'horSai2', 'horEnt3', 'horSai4', 'status']
    search_fields = ['nmEscala', 'horEnt1', 'horSai2', 'horEnt3', 'horSai4', 'status']

admin.site.register(Escala, EscalaAdmin)


class HistRegistroAdmin(admin.ModelAdmin):
    list_display = ('userReg', 'escala', 'dataReg', 'userAlt', 'dataAlt', 'horEnt1', 'horSai2', 'horEnt3', 'horSai4', 'sitAPR')
    search_fields = ('userReg', 'dataReg')
    list_filter = ('userReg', 'dataReg', 'sitAPR')
    per_page = 8
    fieldsets = (
        (None, {
            'fields': ('userReg', 'escala', 'dataReg', 'userAlt', 'dataAlt', 'sitAPR', 'justificativas', 'obsSup')
        }),
        ('Registros', {
            'fields': ('horEnt1', 'horSai2', 'horEnt3', 'horSai4')
        }),
    )
    readonly_fields = ('justificativas',)


admin.site.register(HistRegistro, HistRegistroAdmin)


class TipoJustificativaAdmin(admin.ModelAdmin):
    list_display = ['tipoJustificativa', 'sitJust']
    list_display_links = ['tipoJustificativa', 'sitJust']
    search_fields = ['tipoJustificativa', 'sitJust']

admin.site.register(TipoJustificativa, TipoJustificativaAdmin)


class JustificativaAdmin(admin.ModelAdmin):
    list_display = ['userReg', 'tipoJust', 'data', 'hora']
    list_display_links = ['userReg']
    search_fields = ['userReg', 'tipoJust', 'data', 'hora']

admin.site.register(Justificativa, JustificativaAdmin)

class HoraExtraAdmin(admin.ModelAdmin):
    list_display = ['userExtra', 'dataExtra', 'userAltHe', 'dataAlt', 'horEnt1', 'horSai2', 'horEnt3', 'horSai4', 'sitAPR']
    list_display_links = ['userExtra', 'userAltHe']
    search_fields = ['userExtra', 'userAltHe', 'dataAlt']
    per_page = 8
    fieldsets = (
        (None, {
            'fields': ('userExtra', 'dataExtra', 'userAltHe', 'dataAlt', 'sitAPR', 'justificativas', 'obsSup')
        }),
        ('Registros de Horas Extras', {
            'fields': ('horEnt1', 'horSai2', 'horEnt3', 'horSai4')
        }),
    )
    readonly_fields = ('justificativas',)

admin.site.register(HoraExtra, HoraExtraAdmin)


class EnderecoAdmin(admin.ModelAdmin):
    list_display = ['logradouro', 'numero', 'complemento', 'bairro', 'cidade', 'estado', 'cep']
    list_display_links = ['logradouro']
    search_fields = ['logradouro', 'numero', 'complemento', 'bairro', 'cidade', 'estado', 'cep']

admin.site.register(Endereco, EnderecoAdmin)

class Tipo_FeriadoAdmin(admin.ModelAdmin):
    list_display = ['nmTipo']
    list_display_links = ['nmTipo']
    search_fields = ['nmTipo']

admin.site.register(Tipo_Feriado, Tipo_FeriadoAdmin)

class Level_FeriadoAdmin(admin.ModelAdmin):
    list_display = ['nmLevel', 'endereco']
    list_display_links = ['nmLevel', 'endereco']
    search_fields = ['nmLevel', 'endereco']

admin.site.register(Level_Feriado, Level_FeriadoAdmin)

class FeriadoAdmin(admin.ModelAdmin):
    list_display = ['data', 'nome', 'tipo', 'level']
    list_display_links = ['data', 'nome', 'tipo', 'level']
    search_fields = ['data', 'nome', 'tipo', 'level']

admin.site.register(Feriado, FeriadoAdmin)