from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('homepage/', views.account_home, name='home'),
]