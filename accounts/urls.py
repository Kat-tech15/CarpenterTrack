from django.urls import path
from . import views
from django.contrib.auth imprt views as auth_views


urlpatterns = [
    path('', views.register, name='register'),
    path('accounts/login/',views.login, name='login'),
    path('accounts/logout/', views.logout, name='logout'),
    path('password_reset/', auth_views.PasswordResetViewViews)
]
