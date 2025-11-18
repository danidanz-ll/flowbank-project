from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import Account

@login_required
def account_home(request):
    user = request.user  # CustomUser logado

    # Busca a conta principal do usuário (ex: corrente)
    account = (
        Account.objects.filter(owner=user, is_active=True)
        .order_by('created_at')
        .first()
    )

    context = {
        'nickname': user.nickname or user.email, 
        'balance': account.balance if account else 0, 
    }

    return render(request, 'accounts/home_accounts.html', context)
