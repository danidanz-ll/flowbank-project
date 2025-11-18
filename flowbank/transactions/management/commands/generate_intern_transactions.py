import random
from faker import Faker
from django.core.management.base import BaseCommand
from transactions.models import Transaction, Category
from accounts.models import Account
from decimal import Decimal

# Mapeia o valor do account.account_type (qualquer convenção) para o choice do Transaction
ACCOUNT_TYPE_MAP = ['CORRENTE', 'POUPANCA', 'INVESTIMENTO']

class Command(BaseCommand):
    help = 'Gera transações entre contas do mesmo dono e atualiza saldos. (internas)'

    def handle(self, *args, **options):
        fake = Faker()

        categories = list(Category.objects.all())
        accounts = list(Account.objects.all())

        if not accounts:
            self.stdout.write(self.style.ERROR("❌ Nenhuma conta encontrada no sistema."))
            return

        # -----------------------------------
        # Movimentações internas (mesmo dono)
        # -----------------------------------
        owners = set(acc.owner for acc in accounts)

        for owner in owners:
            user_accounts = [a for a in accounts if a.owner == owner]

            if len(user_accounts) < 2:
                continue  # precisa de mais de uma conta

            for _ in range(random.randint(3, 6)):  # 3–6 movimentações internas
                from_account = random.choice(user_accounts)
                to_account = random.choice([a for a in user_accounts if a != from_account])
                raw = round(random.uniform(10.0, 1000.0), 2)
                amount = Decimal(str(raw))


                if from_account.balance >= amount:
                    from_account.withdraw(amount)
                    to_account.deposit(amount)

                    account_type_from = from_account.account_type
                    account_type_to = to_account.account_type

                    Transaction.objects.create(
                        transaction_type='RETIRADA',
                        amount=amount,
                        from_user=from_account,
                        user_to=to_account,
                        account_type_from=account_type_from,
                        account_type_to=account_type_to,
                        category=random.choice(categories),
                        date=fake.date_between(start_date='-30d', end_date='-5d')
                    )
                else:
                    # se falta saldo, pule essa movimentação interna
                    self.stdout.write(
                        f"⚠️ Saldo insuficiente para retirada interna de {amount} na conta {from_account.account_number}"
                    )

        self.stdout.write("🏦 Movimentações internas concluídas.")