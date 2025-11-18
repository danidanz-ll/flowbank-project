from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from datetime import date
import re

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """Formulário de criação de usuário com validações personalizadas."""

    nickname = forms.CharField(
        required=True, max_length=30, label='Apelido',
        help_text='Como gostaria de ser chamado?',
        widget=forms.TextInput(attrs={'placeholder': 'Naldo'})
    )

    full_name = forms.CharField(
        required=True, max_length=100, label='Nome Completo',
        help_text='Seu nome completo',
        widget=forms.TextInput(attrs={'placeholder': 'Arnaldo Silva'})
    )

    cpf_number = forms.CharField(
        required=True, max_length=14, label='CPF',
        help_text='Use o formato 000.000.000-00',
        widget=forms.TextInput(attrs={'placeholder': '000.000.000-00'})
    )

    email = forms.EmailField(
        required=True, label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'seu.email@dominio.com'})
    )

    birth_date = forms.DateField(
        required=True, label='Data de Nascimento',
        input_formats=['%d/%m/%Y'],
        help_text='Formato: DD/MM/AAAA',
        widget=forms.DateInput(attrs={'placeholder': 'DD/MM/AAAA', 'type': 'text'})
    )

    phone_number = forms.CharField(
        required=True, max_length=20, label='Número de Celular',
        help_text='Inclua o DDD. Exemplo: (11) 98765-4321',
        widget=forms.TextInput(attrs={'placeholder': '(11) 98765-4321'})
    )

    password1 = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'placeholder': '********'})
    )

    password2 = forms.CharField(
        label='Confirme sua senha',
        widget=forms.PasswordInput(attrs={'placeholder': '********'})
    )


    class Meta:
        model = User
        fields = (
            "email", "nickname", "full_name", "cpf_number",
            "birth_date", "phone_number", "password1", "password2"
        )

    # -----------------------------
    # Validações personalizadas
    # -----------------------------

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Este e-mail já está em uso.")
        return email

    def clean_cpf_number(self):
        cpf = self.cleaned_data.get('cpf_number')

        # Verifica formato, mas não o dígito verificador
        pattern = r'^\d{3}\.\d{3}\.\d{3}\-\d{2}$'
        if not re.match(pattern, cpf):
            raise forms.ValidationError("O CPF deve estar no formato 000.000.000-00.")

        if User.objects.filter(cpf_number=cpf).exists():
            raise forms.ValidationError("Este CPF já está cadastrado.")
        return cpf

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date:
            today = date.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            if age < 18:
                raise forms.ValidationError("Você deve ter pelo menos 18 anos para se cadastrar.")
        return birth_date

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        # Aceita formatos como (11) 98765-4321 ou 11987654321
        pattern = r'^\(?\d{2}\)?\s?\d{4,5}\-?\d{4}$'
        if not re.match(pattern, phone):
            raise forms.ValidationError("Número de celular inválido. Use o formato (11) 98765-4321.")
        return phone

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get("email")
        user.nickname = self.cleaned_data.get("nickname", "")
        user.full_name = self.cleaned_data.get("full_name", "")
        user.cpf_number = self.cleaned_data.get("cpf_number") or None
        user.birth_date = self.cleaned_data.get("birth_date")
        user.phone_number = self.cleaned_data.get("phone_number")
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    
    """Formulário de login usando CPF em vez de username/email."""
    username = forms.CharField(
        label='CPF',
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'placeholder': '000.000.000-00',
            'class': 'form-input'
        })
    )

    error_messages = {
    "invalid_login": (
        "Por favor, entre com um CPF e senha corretos. "
        "Note que ambos os campos diferenciam maiúsculas e minúsculas."
    ),
    "inactive": ("Esta conta está inativa."),
    }


    password = forms.CharField(
    label='Senha',
    widget=forms.PasswordInput(attrs={
        'placeholder': '********',
        'class': 'form-input',
        'autocomplete': 'current-password'
    })
    )

    def clean_username(self):
        cpf = self.cleaned_data.get('username')
        # Valida o formato de CPF
        pattern = r'^\d{3}\.\d{3}\.\d{3}\-\d{2}$'
        if not re.match(pattern, cpf):
            raise forms.ValidationError("CPF inválido. Use o formato 000.000.000-00.")
        return cpf
