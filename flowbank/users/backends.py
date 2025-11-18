import re
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class CPFBackend(ModelBackend):
    """Permite autenticação usando o campo cpf_number."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or not password:
            print("⚠️ username ou password ausente")
            return None

        # limpa o CPF para comparar apenas os dígitos
        digits = re.sub(r'\D', '', username)

        # percorre usuários e compara apenas os dígitos
        for user in User.objects.all():
            if not user.cpf_number:
                continue
            db_digits = re.sub(r'\D', '', user.cpf_number)
            if db_digits == digits:
                if user.check_password(password):
                    user.backend = 'users.backends.CPFBackend'
                    return user
                else:
                    print("❌ [CPFBackend] Senha incorreta!")
                    return None

        print("❌ [CPFBackend] Nenhum usuário com CPF correspondente.")
        return None
