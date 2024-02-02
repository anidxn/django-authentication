from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index_page, name='home'),
    path('home/', views.index_page, name='home'),

    path('dash/', views.dash_page, name='dashboard'),
    path('logout/', views.logout_user, name='signout'),

    path('register-user/', views.register_user, name = 'register-user'),
    path('register-user-all/', views.register_user_all, name = 'register-user-all'),
    path('signin/', views.login_user, name = 'signin'),
    path('changepass/', views.changepass_user, name='change-pass'),         # change password without authentication
    path('changepassauth/', views.changepass_withauth, name='change-pass-auth'),     # change password with authentication by old pass
    
    path('profile/', views.update_profile, name='profile')
]