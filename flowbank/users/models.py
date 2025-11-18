from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, EmailValidator
from django.db import models
from datetime import date
import re


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, cpf_number=None, **extra_fields):
        if not email:
            raise ValueError('O email deve ser fornecido')
        email = self.normalize_email(email)
        user = self.model(email=email, cpf_number=cpf_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, cpf_number=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, cpf_number=cpf_number, **extra_fields)


# 🧩 VALIDADORES BÁSICOS

# CPF apenas formato visual
cpf_validator = RegexValidator(
    regex=r'^\d{3}\.\d{3}\.\d{3}\-\d{2}$',
    message="O CPF deve estar no formato 000.000.000-00"
)

# Telefone com DDD
phone_validator = RegexValidator(
    regex=r'^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$',
    message="O número de telefone deve conter DDD + número. Ex: 11 91234-5678"
)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    nickname = models.CharField(max_length=150, blank=True)
    full_name = models.CharField(max_length=100, blank=True)
    cpf_number = models.CharField(
        "CPF",
        max_length=14,
        unique=True,
        null=True,
        blank=True,
        validators=[cpf_validator]
    )
    birth_date = models.DateField("Data de nascimento", null=True, blank=True)
    phone_number = models.CharField(
        "Número de telefone",
        max_length=20,
        blank=True,
        validators=[phone_validator]
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    # 🔎 Validações personalizadas simples
    def clean(self):
        super().clean()

        # --- Validação de idade mínima ---
        if self.birth_date:
            today = date.today()
            age = today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
            )
            if age < 18:
                raise ValidationError({'birth_date': 'O usuário deve ter mais de 18 anos para se cadastrar.'})

        # --- Validação simples de CPF (apenas formato e repetição óbvia) ---
        if self.cpf_number:
            digits = re.sub(r'\D', '', self.cpf_number)
            if digits == digits[0] * len(digits):
                raise ValidationError({'cpf_number': 'CPF inválido (todos os dígitos iguais não são permitidos).'})

        # --- Validação simples de telefone ---
        if self.phone_number:
            only_digits = re.sub(r'\D', '', self.phone_number)
            if len(only_digits) not in [10, 11]:
                raise ValidationError({'phone_number': 'O número deve conter DDD + número (10 ou 11 dígitos).'})
