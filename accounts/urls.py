from django.urls import path
from .views import LoginView,LogoutView,CadastroView,DashboardView

urlpatterns = [
    path('',LoginView.as_view(template_name='accounts/login.html'),name='index_login'),
    path('login/',LoginView.as_view(template_name='accounts/login.html'),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('cadastro/',CadastroView.as_view(template_name='accounts/cadastro.html'),name='cadastro'),
    path('dashboard/',DashboardView.as_view(template_name='accounts/dashboard.html'),name='dashboard'),
]
