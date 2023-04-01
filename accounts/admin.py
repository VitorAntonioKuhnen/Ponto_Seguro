from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Users, Token

class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('username', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    per_page = 11
    fieldsets = (
        (None, {
            'fields': ('username', 'matricula', 'password', 'first_name', 'last_name', 'email', 'is_active')
        }),
        ('Datas Importantes', {
            'fields': ('last_login', 'date_joined', 'dt_troca_senha')
        }),
    )


admin.site.register(Users, UsuarioAdmin)


class TokenAdmin(admin.ModelAdmin):
    list_display = ['codToken', 'usuario', 'datGer', 'horGer']
    list_display_links = ['codToken', 'usuario']
    search_fields = ['codToken', 'usuario', 'datGer', 'horGer']

admin.site.register(Token, TokenAdmin)