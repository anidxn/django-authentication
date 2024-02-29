from django.urls import path, include
from . import views

# * * * * * * Builtin Views for Password Reset * * * * * *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index_page, name='home'),
    path('home/', views.index_page, name='home'),

    path('dash/', views.dash_page, name='dashboard'),
    path('logout/', views.logout_user, name='signout'),

    path('register-user/', views.register_user, name = 'register-user'),
    path('register-user-all/', views.register_user_all, name = 'register-user-all'),

    path('register-verify/', views.register_verify, name = 'register-verify'),
    path('activate/<uidb64>/<token>', views.activate_user, name = 'activate'),

    path('signin/', views.login_user, name = 'signin'),
    path('changepass/', views.changepass_user, name='change-pass'),         # change password without authentication
    path('changepassauth/', views.changepass_withauth, name='change-pass-auth'),     # change password with authentication by old pass
    
    path('profile/', views.update_profile, name='profile'),

    #----------- Class based views for password reset ------------
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='reset_password1'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='reset_password2'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view())
]

'''
Forgot password======================
CONDITION: the email you will enter in the form , that email must belong to 1 of the registered USERS
1. submit email form                        PasswordRest
2. Email sent success message
3. Link to password reset form in email
4. Password successfully changed message

'''