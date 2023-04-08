from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Escala, HistRegistro, Justificativa, TipoJustificativa


class EscalaAdmin(admin.ModelAdmin):
    list_display = ['nmEscala', 'horaEntM', 'horaSaiM', 'horaEntV', 'horaSaiV', 'status']
    list_display_links = ['nmEscala', 'horaEntM', 'horaSaiM', 'horaEntV', 'horaSaiV', 'status']
    search_fields = ['nmEscala', 'horaEntM', 'horaSaiM', 'horaEntV', 'horaSaiV', 'status']

admin.site.register(Escala, EscalaAdmin)


class HistRegistroAdmin(admin.ModelAdmin):
    list_display = ('userReg', 'escala', 'dataReg', 'horaEntM', 'horaSaiM', 'horaEntV', 'horaSaiV', 'bancoHora', 'sitAPR')
    search_fields = ('userReg', 'dataReg')
    list_filter = ('userReg', 'dataReg', 'sitAPR')
    per_page = 8
    fieldsets = (
        (None, {
            'fields': ('userReg', 'escala', 'dataReg', 'bancoHora', 'sitAPR')
        }),
        ('Registros', {
            'fields': ('horaEntM', 'horaSaiM', 'horaEntV', 'horaSaiV')
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