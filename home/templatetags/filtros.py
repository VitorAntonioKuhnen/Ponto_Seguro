from django import template


register = template.Library()

@register.filter
def no_grupo(user, nome_grupo):
    return user.groups.filter(name=nome_grupo).exists()