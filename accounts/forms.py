
from django import forms
from django.contrib.auth.models import User
from .models import Profile

class CustomRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(max_length=128, widget=forms.PasswordInput, label='Contraseña')
    password2 = forms.CharField(max_length=128, widget=forms.PasswordInput, label='Confirmar contraseña')
    photo = forms.ImageField(label='Foto de perfil', required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado.')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.set_password(self.cleaned_data['password1'])
            user.save()
            # Crear el perfil del usuario
            photo = self.cleaned_data.get('photo')
            Profile.objects.create(user=user, photo=photo)
        return user