from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Cargo, Users, Token

class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'dat_admissao', 'dat_inicia_trab', 'superior', 'is_staff', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'dat_admissao', 'dat_inicia_trab', 'superior')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    per_page = 16
    fieldsets = (
        (None, {
            'fields': ('foto','username', 'matricula', 'password', 'first_name', 'last_name', 'email', 'superior', 'cargo', 'endereco',         'is_active', 'is_staff', 'groups')
        }),
        ('Registros', {
            'fields': ('escala', 'justificar', 'hora_extra')
        }),
        ('Datas Importantes', {
            'fields': ('dat_admissao', 'dat_inicia_trab', 'dt_troca_senha', 'last_login', 'date_joined')
        }),
    )


admin.site.register(Users, UsuarioAdmin)


class TokenAdmin(admin.ModelAdmin):
    list_display = ['codToken', 'usuario', 'datGer', 'horGer']
    list_display_links = ['codToken', 'usuario']
    search_fields = ['codToken', 'usuario', 'datGer', 'horGer']

admin.site.register(Token, TokenAdmin)

class CargoAdmin(admin.ModelAdmin):
    list_display = ['nmCargo', 'sitCargo']
    list_display_links = ['nmCargo', 'sitCargo']
    search_fields = ['nmCargo', 'sitCargo']

admin.site.register(Cargo, CargoAdmin)