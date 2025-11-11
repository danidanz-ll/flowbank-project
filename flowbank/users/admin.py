from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import UserChangeForm

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = '__all__'

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('cpf_number','email','nickname','full_name', 'is_staff')
    ordering = ('cpf_number',)
    fieldsets = (
        (None, {'fields': ('cpf_number', 'password')}),
        ('Informações Pessoais', {'fields': ('nickname', 'full_name', 'email')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('cpf_number', 'email', 'nickname', 'full_name', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)