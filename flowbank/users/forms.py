from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """Form de criação de usuário personalizado.

    Usa `email` como campo principal de identificação.
    """
    nickname = forms.CharField(
        required=True, max_length=30, label='Apelido', help_text='Como gostaria de ser chamado?',
    )
    full_name = forms.CharField(
        required=True, max_length=30, label='Nome Completo', help_text='Seu nome completo'
    )
    cpf_number = forms.CharField(
        required=True, max_length=14, label='CPF', help_text='Seu CPF formato 000.000.000-00'
    )
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ("email", "nickname", "full_name", "cpf_number", "password1", "password2")
        widgets = {
            'nickname': forms.TextInput(attrs={'placeholder': 'Naldo'}),
            'full_name': forms.TextInput(attrs={'placeholder': 'Arnaldo Silva'}),
            'cpf_number': forms.TextInput(attrs={'placeholder': '000.000.000-00'}),
            'email': forms.EmailInput(attrs={'placeholder': 'seu.email@dominio.com'}),
            'password1': forms.PasswordInput(attrs={'placeholder': '********'}),
            'password2': forms.PasswordInput(attrs={'placeholder': '********'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Este e‑mail já está em uso.")
        return email

    def clean_cpf_number(self):
        cpf = self.cleaned_data.get('cpf_number')
        if cpf and User.objects.filter(cpf_number=cpf).exists():
            raise forms.ValidationError("Este CPF já está cadastrado.")
        return cpf

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get("email")
        user.nickname = self.cleaned_data.get("nickname", "")
        user.full_name = self.cleaned_data.get("full_name", "")
        user.cpf_number = self.cleaned_data.get("cpf_number") or None
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    """Authentication form that shows 'Email' as the label instead of 'Username'.

    The underlying AuthenticationForm still posts the value as 'username', which
    Django's authentication backend accepts; the label is changed for clarity.
    """
    username = forms.CharField(
        label='Email',
        widget=forms.EmailInput(attrs={'autofocus': True, 'placeholder': 'seu.email@dominio.com'})
    )
