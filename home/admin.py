from django.contrib import admin
from .models import Token

class TokenAdmin(admin.ModelAdmin):
    list_display = ['codToken', 'usuario', 'datGer', 'horGer']
    list_display_links = ['codToken', 'usuario']
    search_fields = ['codToken', 'usuario', 'datGer', 'horGer']

admin.site.register(Token, TokenAdmin)