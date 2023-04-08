from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Users, Token

class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'dat_admissao', 'dat_inicia_trab', 'is_staff', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'dat_admissao', 'dat_inicia_trab',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    per_page = 15
    fieldsets = (
        (None, {
            'fields': ('foto','username', 'matricula', 'password', 'first_name', 'last_name', 'email', 'is_active')
        }),
        ('Registros', {
            'fields': ('escala', 'justificar')
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