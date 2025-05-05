from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    
    autor_username = serializers.CharField(source='autor.username', read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'autor',
            'autor_username',
            'titulo',
            'contenido',
            'creado',
            'imagen',
            'aprobado',
           
        ]