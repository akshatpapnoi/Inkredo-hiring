from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('register', views.register, name='register'),
    path('company/login', views.company_login, name='company-login'),
    path('company/register', views.company_register, name='company-register'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('company/dashboard', views.company_dashboard, name='company-dashboard'),
]
