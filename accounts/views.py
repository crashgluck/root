from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
# accounts/views.py

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404

from .models import Profile
#from .models import Profile
from .forms import CustomRegistrationForm, CrearGrupoForm, AsignarUsuarioAGrupoForm
from django.contrib.auth.models import User, Group

from rest_framework import viewsets


from django.contrib.auth.models import User
from .serializers import UserSerializer

# accounts/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer


# Create your views here.
def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                
                # Verificar si el usuario pertenece a un grupo específico
                if user.groups.filter(name='administrativo').exists():
                    return redirect('index')  # Redirigir a la vista específica del grupo
                else:
                    return redirect('index')  # Redirigir a la vista por defecto
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form':form})



def user_logout(request):
    logout(request)
    return redirect('login_user')





def register(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Extraer los datos del formulario
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password2']
            photo = form.cleaned_data.get('photo')

            # Crear el usuario
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            # Verificar si el perfil ya existe para este usuario
            profile, created = Profile.objects.get_or_create(user=user)

            # Solo actualiza el perfil si se ha creado uno nuevo
            if created:
                profile.photo = photo
                profile.save()

            # Iniciar sesión automáticamente (opcional)
            login(request, user)

            # Redirigir a una página de éxito o a la página de inicio de sesión
            return redirect('login_user')
    else:
        form = CustomRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})



def es_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(lambda u: u.is_superuser)
def lista_usuarios(request):
    usuarios = User.objects.all().select_related()
    grupos = Group.objects.all()
    asignar_form = AsignarUsuarioAGrupoForm()
    crear_grupo_form = CrearGrupoForm()

    if request.method == 'POST':
        if 'asignar_usuario' in request.POST:
            asignar_form = AsignarUsuarioAGrupoForm(request.POST)
            if asignar_form.is_valid():
                usuario = asignar_form.cleaned_data['usuario']
                grupo = asignar_form.cleaned_data['grupo']
                grupo.user_set.add(usuario)
                return redirect('lista_usuarios')

        elif 'crear_grupo' in request.POST:
            crear_grupo_form = CrearGrupoForm(request.POST)
            if crear_grupo_form.is_valid():
                crear_grupo_form.save()
                return redirect('lista_usuarios')

    return render(request, 'accounts/lista_usuarios.html', {
        'usuarios': usuarios,
        'grupos': grupos,
        'asignar_form': asignar_form,
        'crear_grupo_form': crear_grupo_form
    })

@login_required
@user_passes_test(es_superuser)
def activar_usuario(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = True
    user.save() 
    return redirect('lista_usuarios')

@login_required
@user_passes_test(es_superuser)
def desactivar_usuario(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = False
    user.save()
    return redirect('lista_usuarios')

@login_required
@user_passes_test(es_superuser)
def eliminar_usuario(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('lista_usuarios')


class UserListAPIView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)