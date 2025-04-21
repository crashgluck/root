from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name="login_user"),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
  ]
