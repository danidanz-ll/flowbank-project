from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,BaseUserManager
from django.db import models

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
    
                user = self.create_user(email, password, **extra_fields)
                return user
        
class CustomUser(AbstractBaseUser,PermissionsMixin):
        email = models.EmailField(unique=True)
        nickname = models.CharField(max_length=150, blank=True)
        full_name = models.CharField(max_length=100, blank=True)
        cpf_number = models.CharField(max_length=14, unique=True, null=True, blank=True)
        is_staff = models.BooleanField(default=False)
        is_active = models.BooleanField(default=True)

        # Make email the field used for authentication
        USERNAME_FIELD = 'email'
        # Empty REQUIRED_FIELDS means only email and password are prompted for superuser creation
        REQUIRED_FIELDS = []
        objects = CustomUserManager()


        def __str__(self):
                return self.email