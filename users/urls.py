from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('login/', views.LoginPage.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password-change/', views.PasswordChange.as_view(template_name='users/password_change.html'), name='change_password'),
]
