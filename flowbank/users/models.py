from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
       def create_user(self, cpf_number, email, password, **extra_fields):
               if not cpf_number:
                       raise ValueError('O CPF deve ser fornecido')
               email = self.normalize_email(email)
               user = self.model(cpf_number=cpf_number, email=email, **extra_fields)
               user.set_password(password)
               user.save()
               return user
       def create_superuser(self, cpf_number, email, password, **extra_fields):
                extra_fields.setdefault('is_staff', True)
                extra_fields.setdefault('is_superuser', True)
    
                if extra_fields.get('is_staff') is not True:
                          raise ValueError('Superuser must have is_staff=True.')
                if extra_fields.get('is_superuser') is not True:
                          raise ValueError('Superuser must have is_superuser=True.')
    
                user = self.create_user(cpf_number, email, password, **extra_fields)
                return user
        
class CustomUser(AbstractBaseUser,PermissionsMixin):
        email = models.EmailField(unique=True)
        nickname = models.CharField(max_length=150)
        full_name = models.CharField(max_length=100)
        cpf_number = models.CharField(max_length=14, unique=True)
        is_staff = models.BooleanField(default=False)
        is_active = models.BooleanField(default=True)

        # Make cpf_number the field used for authentication
        USERNAME_FIELD = 'cpf_number'
        # When creating a superuser via `createsuperuser`, Django will prompt for these
        REQUIRED_FIELDS = ['email']

        objects = CustomUserManager()


        def __str__(self):
                return self.email