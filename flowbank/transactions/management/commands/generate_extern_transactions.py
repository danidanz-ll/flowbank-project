import random
from faker import Faker
from django.core.management.base import BaseCommand
from transactions.models import Transaction, Category
from accounts.models import Account
from decimal import Decimal

# Mapeia o valor do account.account_type (qualquer convenção) para o choice do Transaction
ACCOUNT_TYPE_MAP = ['CORRENTE', 'POUPANCA', 'INVESTIMENTO']

class Command(BaseCommand):
    help = 'Gera transações externas (donos diferentes) e atualiza saldos.'

    def handle(self, *args, **options):
        fake = Faker()


        categories = list(Category.objects.all())
        accounts = list(Account.objects.all())

        if not accounts:
            self.stdout.write(self.style.ERROR("❌ Nenhuma conta encontrada no sistema."))
            return

        # -----------------------------------
        # Movimentações externas (entre donos diferentes) — SAÍDA SÓ DE CONTAS CORRENTES
        # -----------------------------------
        # filtra contas que são do tipo "corrente" (levando em conta variações)

        corrent_accounts = [acc for acc in accounts if acc.account_type.upper() == 'CORRENTE']
        
        if not corrent_accounts:
            self.stdout.write(self.style.WARNING("⚠️ Não há contas correntes para realizar transferências externas."))
        else:
            attempts = 0
            created = 0
            # queremos até N transferências externas, mas limitar tentativas para evitar loop infinito
            TARGET_EXTERNAL = 30
            MAX_ATTEMPTS = 80

            while created < TARGET_EXTERNAL and attempts < MAX_ATTEMPTS:
                attempts += 1
                from_account = random.choice(corrent_accounts)
                to_account = random.choice(corrent_accounts)

                # evita transferir para si mesmo e garante donos diferentes
                if from_account.owner == to_account.owner:
                    continue
                
                raw = round(random.uniform(100.0, 800.0), 2)
                amount = Decimal(str(raw))

                # só permite se houver saldo
                if from_account.balance >= amount:
                    from_account.withdraw(amount)
                    to_account.deposit(amount)

                    Transaction.objects.create(
                        transaction_type='RETIRADA',
                        amount=amount,
                        from_user=from_account,
                        user_to=to_account,
                        account_type_from='CORRENTE',
                        account_type_to='CORRENTE',
                        category=random.choice(categories),
                        date=fake.date_between(start_date='-5d', end_date='today')
                    )
                    created += 1
                else:
                    continue

            self.stdout.write(f"🔁 Tentativas externas: {attempts}, transferências externas criadas: {created}")

