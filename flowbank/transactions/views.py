from django.shortcuts import render
from django.db.models import Q
from transactions.models import Transaction
from accounts.models import Account
from django.utils import timezone
from django.db.models import Sum

def historic_transactions(request):
    # pega a conta do usuário logado
    account = Account.objects.get(owner=request.user,account_type='CORRENTE')
    now = timezone.now()

    # filtra transações enviadas e recebidas
    user_transactions = Transaction.objects.filter(
        Q(from_user=account) | Q(user_to=account)
    ).order_by('-date')

    # Filtrar transações enviadas pelo usuário no mês atual
    monthly_expenses = (
    Transaction.objects.filter(
        from_user=account,
        date__year=now.year,
        date__month=now.month
    )
    .aggregate(total=Sum('amount'))['total'] or 0
    )

    return render(request, 'transactions/historic_transactions.html', {
        'monthly_expenses': monthly_expenses,
        'account': account,
        'user_transactions': user_transactions,
    })
