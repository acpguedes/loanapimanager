"""loanapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from loanapi.core import views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    url(r'^login/$',
        auth_views.LoginView.as_view(template_name="login.html"),
        {'template_name': 'login.html'},
        name='login'),
    url(r'^logout/$',
        auth_views.LogoutView.as_view(),
        name='logout'),
    path("", views.home, name="home"),
    path('api-token-auth/', views.CustomAuthToken.as_view(), name='token'),
    path('json/loans/', views.LoanView.as_view(), name='loans'),
    path('json/payments/', views.PaymentView.as_view(), name='payments'),
    path('create/loan', views.create_loan, name='loancreator'),
    path('create/payment', views.create_payment, name='paymentcreator'),
]
