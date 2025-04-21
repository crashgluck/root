from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    titulo = models.CharField(max_length=255)
    contenido = models.TextField()
    creado = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='posts/imagenes_subidas/', blank=True, null=True)  # <-- aquí
    aprobado = models.BooleanField(default=False)  # <-- nuevo campo

    def __str__(self):
        return self.titulo

    def total_likes(self):
        return self.likes.count()

    def promedio_puntuacion(self):
        puntuaciones = self.puntuaciones.all()
        if puntuaciones.exists():
            return sum(p.valor for p in puntuaciones) / puntuaciones.count()
        return 0

class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentario por {self.autor}'

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'usuario')  # Un usuario solo puede dar un like por post

    def __str__(self):
        return f'{self.usuario} dio like a "{self.post}"'

class Puntuacion(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='puntuaciones')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    valor = models.PositiveSmallIntegerField()  # Por ejemplo: de 1 a 5

    class Meta:
        unique_together = ('post', 'usuario')  # Una puntuación por usuario y post

    def __str__(self):
        return f'{self.usuario} puntuó "{self.post}" con {self.valor}'


class Favorito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='favoritos', on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'post')  # Evita favoritos duplicados