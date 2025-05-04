from django import template

register = template.Library()

@register.filter(name='en_grupo')
def en_grupo(usuario, nombre_grupo):
    return usuario.groups.filter(name=nombre_grupo).exists()
