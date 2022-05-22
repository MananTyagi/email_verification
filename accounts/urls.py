from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('success/', views.success, name='success'),
    path('token_send/', views.token_send, name='token_send'),
    path('verify/<auth_token>', views.verify, name='verify'),
    path('reset_verify/<auth_token>', views.reset_verify, name='reset_verify'),
    path('error/', views.error, name='error'),
    path('reset/', views.reset_password, name='reset'),
]