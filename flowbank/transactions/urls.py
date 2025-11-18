from django.urls import path, include, re_path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve

app_name = 'transactions'

urlpatterns = [
    path('hist_transactions/', views.historic_transactions, name='historic_transactions'),
]
