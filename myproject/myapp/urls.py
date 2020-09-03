from django.urls import path
from .import views

from django.contrib.auth import views as auth_views # this is for password reset

urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),

    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('user/', views.userPage, name='user'),
    path('product/', views.products, name='prducts'),
    path('customer/<str:pk>/', views.customers, name='customer'),
    path('account/', views.accountSettings, name='settings'),

    path('create_issue/<str:pk>/', views.createIssue, name='create_issue'),
    path('update_issue/<str:pk>/', views.updateIssue, name='update_issue'),
    path('delete_issue/<str:pk>/', views.deleteIssue, name='delete_issue'),

    # belows are for password reset
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name = "myapp/password_reset.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = "myapp/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = "myapp/password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "myapp/password_reset_done.html"), name="password_reset_complete"),
]

