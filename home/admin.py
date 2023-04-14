from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Escala, HistRegistro, Justificativa, TipoJustificativa, HoraExtra


class EscalaAdmin(admin.ModelAdmin):
    list_display = ['nmEscala', 'horEnt1', 'horSai2', 'horEnt3', 'horSai4', 'status']
    list_display_links = ['nmEscala', 'horEnt1', 'horSai2', 'horEnt3', 'horSai4', 'status']
    search_fields = ['nmEscala', 'horEnt1', 'horSai2', 'horEnt3', 'horSai4', 'status']

admin.site.register(Escala, EscalaAdmin)


class HistRegistroAdmin(admin.ModelAdmin):
    list_display = ('userReg', 'escala', 'dataReg', 'horEnt1', 'horSai2', 'horEnt3', 'horSai4', 'bancoHoraMin', 'sitAPR')
    search_fields = ('userReg', 'dataReg')
    list_filter = ('userReg', 'dataReg', 'sitAPR')
    per_page = 8
    fieldsets = (
        (None, {
            'fields': ('userReg', 'escala', 'dataReg', 'bancoHoraMin', 'sitAPR')
        }),
        ('Registros', {
            'fields': ('horEnt1', 'horSai2', 'horEnt3', 'horSai4')
        }),
    )


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
    list_display = ['userExtra', 'dataExtra', 'userLib', 'dataLib', 'horEnt1', 'horSai2', 'horEnt3', 'horSai4', 'sitApr']
    list_display_links = ['userExtra', 'userLib']
    search_fields = ['userExtra', 'userLib', 'dataLib']
    per_page = 8
    fieldsets = (
        (None, {
            'fields': ('userExtra', 'dataExtra', 'userLib', 'dataLib', 'sitApr')
        }),
        ('Registros de Horas Extras', {
            'fields': ('horEnt1', 'horSai2', 'horEnt3', 'horSai4')
        }),
    )

admin.site.register(HoraExtra, HoraExtraAdmin)