import random
from faker import Faker
from django.core.management.base import BaseCommand
from transactions.models import Transaction, Category
from accounts.models import Account
from decimal import Decimal

class Command(BaseCommand):
    help = 'Gera depósitos em contas e atualiza saldos.'

    def handle(self, *args, **options):
        fake = Faker()

        categories = list(Category.objects.all())
        accounts = list(Account.objects.all())

        if not accounts:
            self.stdout.write(self.style.ERROR("❌ Nenhuma conta encontrada no sistema."))
            return

        # -----------------------------------
        # 1️⃣ Depósitos iniciais
        # -----------------------------------
        for account in accounts:
            amount_raw = round(random.uniform(100.0, 1000.0), 2)
            deposit_amount = Decimal(amount_raw)

            # Usa o tipo de conta real do objeto Account
            account_type_from = account.account_type
            account_type_to = account.account_type

            # Faz o depósito diretamente
            account.deposit(deposit_amount)

            # Cria a transação representando esse depósito
            Transaction.objects.create(
                transaction_type='DEPOSITO',
                amount=deposit_amount,
                from_user=account,
                user_to=account,
                account_type_from=account_type_from,
                account_type_to=account_type_to,
                category=random.choice(categories) if categories else None,
                date=fake.date_between(start_date='-60d', end_date='-30d')
            )

        self.stdout.write(self.style.SUCCESS("💰 Depósitos iniciais criados com sucesso."))
