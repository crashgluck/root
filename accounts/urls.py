from django.urls import path
from . import views


from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('login/', views.login_user, name="login_user"),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/activar/<int:user_id>/', views.activar_usuario, name='activar_usuario'),
    path('usuarios/desactivar/<int:user_id>/', views.desactivar_usuario, name='desactivar_usuario'),
    path('usuarios/eliminar/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
     path('api/users/', views.UserListAPIView.as_view(), name='api-users'),
  ]