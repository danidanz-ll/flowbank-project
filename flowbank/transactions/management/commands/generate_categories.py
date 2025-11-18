import random
from faker import Faker
from django.core.management.base import BaseCommand
from transactions.models import Transaction, Category
from accounts.models import Account
from decimal import Decimal

# Mapeia o valor do account.account_type (qualquer convenção) para o choice do Transaction
ACCOUNT_TYPE_MAP = [
        ('CORRENTE', 'Conta Corrente'),
        ('POUPANCA', 'Conta Poupança'),
        ('INVESTIMENTO', 'Conta Investimento'),
    ]

class Command(BaseCommand):
    help = 'Gera categorias de transação.'

    def handle(self, *args, **options):
        fake = Faker()

        # -----------------------------------
        # Cria categorias padrão se não existirem
        # -----------------------------------
        categories = [
            'Contas', 'Alimentação', 'Lazer', 'Transporte',
            'Saúde', 'Educação', 'Roupas', 'Cosméticos', 'Poupança','Investimentos'
        ]
        for category_name in categories:
            Category.objects.get_or_create(name=category_name)