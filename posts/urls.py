from django.urls import path
from . import views

urlpatterns = [
    path('post/', views.post, name='post'),
    path('favoritos/', views.favoritos, name='favoritos'),
    path('nuevo-post/', views.crear_post, name='crear_post'),  
    path('comentarios/<int:post_id>/', views.comentar_post, name='comentar_post'),
    path('post/<int:post_id>/like/', views.toggle_like, name='like_post'),
    path('post/<int:post_id>/favorito/', views.toggle_favorito, name='toggle_favorito'),
    path('toggle_aprobado/', views.toggle_aprobado, name='toggle_aprobado'),

]
