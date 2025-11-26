from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/',views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),  
    path('profile/', views.profile, name='profile'),  
    path('messages/', views.admin_messages, name='admin_messages'),
    path('messages/respond/<int:message_id>/', views.reply_message, name='reply_message'),  
    path('create-superuser/', views.create_superuser),

]
