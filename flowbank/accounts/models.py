import random
from django.db import models
from django.utils import timezone
from django.conf import settings

def generate_account_number():
    """Gera um número de conta aleatório e único no formato XXXXXXX-YY."""
    base = str(random.randint(1000000, 9999999))
    suffix = str(random.randint(10, 99))
    return f"{base}-{suffix}"

class Account(models.Model):
    ACCOUNT_TYPES = [
        ('CORRENTE', 'Conta Corrente'),
        ('POUPANCA', 'Conta Poupança'),
        ('INVESTIMENTO', 'Conta Investimento'),
    ]

    account_number = models.CharField(max_length=20, unique=True, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='accounts'
    )
    account_type = models.CharField(
        max_length=20, 
        choices=ACCOUNT_TYPES, 
        default='CORRENTE'
    )
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Conta'
        verbose_name_plural = 'Contas'
        unique_together = ('owner', 'account_type')

    def __str__(self):
        return f"{self.get_account_type_display()} ({self.account_number}) - {self.owner}"

    def save(self, *args, **kwargs):
        """Gera um número único de conta automaticamente."""
        if not self.account_number:
            new_number = generate_account_number()
            while Account.objects.filter(account_number=new_number).exists():
                new_number = generate_account_number()
            self.account_number = new_number
        super().save(*args, **kwargs)

    # Métodos de movimentação
    def deposit(self, amount):
        self.balance += amount
        self.save(update_fields=['balance'])

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Saldo insuficiente.")
        self.balance -= amount
        self.save(update_fields=['balance'])

    
