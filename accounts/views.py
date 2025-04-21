from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate

from .models import Profile
#from .models import Profile
from .forms import CustomRegistrationForm
from django.contrib.auth.models import User

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
            return redirect('login')
    else:
        form = CustomRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})

