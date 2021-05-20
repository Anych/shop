from django.urls import path

from accounts import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('confirm_email/', views.confirm_email, name='confirm_email'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('activate/<uidb64>/<token>/<email>/', views.activate, name='activate'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),

    path('change_password/', views.change_password, name='change_password'),
]
