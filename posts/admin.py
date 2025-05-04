from django.contrib import admin
from .models import Post, Comentario, Like, Puntuacion, Favorito

admin.site.register(Post)
admin.site.register(Comentario)
admin.site.register(Like)
admin.site.register(Puntuacion)
admin.site.register(Favorito)
