from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = '__all__'

class CustomUserAdminCreationForm(UserCreationForm):
    """Admin form for creating users - CPF is optional for admin/superusers."""
    email = forms.EmailField(required=True, label='Email')
    nickname = forms.CharField(
        required=False, max_length=150, label='Apelido'
    )
    full_name = forms.CharField(
        required=False, max_length=100, label='Nome Completo'
    )
    cpf_number = forms.CharField(
        required=False, max_length=14, label='CPF', 
        help_text='Opcional para administradores. Obrigatório para usuários regulares.'
    )

    class Meta:
        model = CustomUser
        fields = ("email", "nickname", "full_name", "cpf_number", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and CustomUser.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Este e‑mail já está em uso.")
        return email

    def clean_cpf_number(self):
        cpf = self.cleaned_data.get('cpf_number')
        if cpf and CustomUser.objects.filter(cpf_number=cpf).exists():
            raise forms.ValidationError("Este CPF já está cadastrado.")
        return cpf or None

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserAdminCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email','cpf_number','nickname','full_name', 'is_staff')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('nickname', 'full_name', 'cpf_number')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'cpf_number', 'nickname', 'full_name', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)