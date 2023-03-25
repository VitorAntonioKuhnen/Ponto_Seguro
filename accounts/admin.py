from django.contrib import admin
from .models import User

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    per_page = 11
    fieldsets = (
        (None, {
            'fields': ('username', 'matricula', 'password', 'first_name', 'last_name', 'email')
        }),
        ('Datas Importantes', {
            'fields': ('last_login', 'date_joined', 'dt_troca_senha')
        }),
    )


admin.site.register(User, UsuarioAdmin)