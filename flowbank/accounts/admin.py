from django.contrib import admin
from .models import Account

# Register your models here.
@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('account_number', 'owner', 'account_type', 'balance', 'is_active', 'created_at')
    list_filter = ('account_type', 'is_active')
    search_fields = ('account_number', 'owner__email', 'owner__nickname')