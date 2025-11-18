from django.contrib import admin
from .models import Transaction, Category


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'transaction_id',
        'transaction_type',
        'amount',
        'from_user_display',
        'user_to_display',
        'account_type_from',
        'account_type_to',
        'category',
        'date',
    )
    list_filter = (
        'transaction_type',
        'account_type_from',
        'account_type_to',
        'category',
        'date',
    )
    search_fields = (
        'from_user__account_number',
        'user_to__account_number',
        'category__name',
    )
    ordering = ('-date',)
    list_per_page = 20

    # Campos de exibição customizados
    def from_user_display(self, obj):
        """Mostra número da conta e dono resumido"""
        return f"{obj.from_user.account_number} ({obj.from_user.owner.nickname if hasattr(obj.from_user.owner, 'nickname') else obj.from_user.owner.email})"
    from_user_display.short_description = "De (Conta / Dono)"

    def user_to_display(self, obj):
        """Mostra número da conta e dono resumido"""
        return f"{obj.user_to.account_number} ({obj.user_to.owner.nickname if hasattr(obj.user_to.owner, 'nickname') else obj.user_to.owner.email})"
    user_to_display.short_description = "Para (Conta / Dono)"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
