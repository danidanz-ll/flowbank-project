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
    """Formulário para criação de usuários no Admin."""
    email = forms.EmailField(required=True, label='Email')
    nickname = forms.CharField(required=False, max_length=150, label='Apelido')
    full_name = forms.CharField(required=False, max_length=100, label='Nome Completo')
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
            raise forms.ValidationError("Este e-mail já está em uso.")
        return email

    def clean_cpf_number(self):
        cpf = self.cleaned_data.get('cpf_number')
        if cpf and CustomUser.objects.filter(cpf_number=cpf).exists():
            raise forms.ValidationError("Este CPF já está cadastrado.")
        return cpf or None


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserAdminCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    # 🧩 Campos exibidos na listagem principal do admin
    list_display = (
        'email', 'full_name', 'nickname', 'cpf_number', 
        'birth_date', 'phone_number', 'is_staff'
    )
    search_fields = ('email', 'full_name', 'cpf_number', 'nickname')
    ordering = ('email',)

    # 📑 Agrupamento dos campos dentro da edição do usuário
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {
            'fields': ('full_name', 'nickname', 'cpf_number', 'birth_date', 'phone_number')
        }),
        ('Permissões', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Datas Importantes', {'fields': ('last_login',)}),
    )

    # ⚙️ Campos exibidos ao criar um novo usuário no admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'cpf_number', 'nickname', 'full_name',
                'birth_date', 'phone_number',
                'password1', 'password2', 
                'is_staff', 'is_superuser'
            ),
        }),
    )
