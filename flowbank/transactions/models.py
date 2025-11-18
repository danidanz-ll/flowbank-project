from django.db import models
import uuid

class Category(models.Model):
    name = models.CharField(max_length=50, unique = True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
    

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('DEPOSITO', 'Depósito'),
        ('RETIRADA', 'Retirada'),
    ]

    ACCOUNT_TYPE_CHOICES = [
        ('CORRENTE', 'Conta Corrente'),
        ('POUPANCA', 'Conta Poupança'),
        ('INVESTIMENTO', 'Conta Investimento'),
    ]

    transaction_id = models.CharField(max_length=20, primary_key=True, unique=True, editable=False)
    transaction_type = models.CharField(max_length=15, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    from_user = models.ForeignKey('accounts.Account', on_delete=models.CASCADE, related_name='transactions_from')
    user_to = models.ForeignKey('accounts.Account', on_delete=models.CASCADE, related_name='transactions_to')
    account_type_from = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES)
    account_type_to = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            # Gera um código curto e único, ex: TRX-AB12CD34
            unique_part = uuid.uuid4().hex[:8].upper()
            self.transaction_id = f"TRX-{unique_part}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return (
            f"{self.transaction_id} -- "
            f"{self.transaction_type} - R${self.amount} | "
            f"De: {self.from_user} ({self.account_type_from}) "
            f"→ Para: {self.user_to} ({self.account_type_to}) "
            f"em {self.date.strftime('%d/%m/%Y %H:%M')}"
            f" | Categoria: {self.category.name if self.category else 'N/A'}"
        )

 