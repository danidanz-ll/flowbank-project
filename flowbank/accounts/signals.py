from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Account

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_default_accounts(sender, instance, created, **kwargs):
    if created:
        default_account_types = ['CORRENTE', 'POUPANCA', 'INVESTIMENTO']
        for acc_type in default_account_types:
            Account.objects.create(owner=instance, account_type=acc_type)
