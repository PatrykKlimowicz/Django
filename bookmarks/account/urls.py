from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    # custom login view:
    # path('login/', views.user_login, name='login'),

    # login/out views provided by Django:
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # application views
    path('', views.dashboard, name='dashboard'),

    # changing password
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # resetting password
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # register user
    path('register/', views.user_register, name='register'),

    # edit user data
    path('edit/', views.edit_user, name='edit'),
]
