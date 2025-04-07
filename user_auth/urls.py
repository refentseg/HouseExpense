from django.urls import path

from user_auth import views

"""
URL configuration for the user authentication app.

This module contains URL patterns for handling user authentication operations
including login, registration, user creation and authentication.


:routes:
    /: Displays the login page (views.user_login)
    /register/: Displays the user registration form (views.user_register)
    /create_user/: Processes user creation after form submission
                   (views.create_user)
    /authenticate_user/: Handles authentication of user credentials
                         (views.authenticate_user)
"""
app_name = 'user_auth'
urlpatterns = [
    path('', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('create_user/', views.create_user, name='create_user'),
    path('authenticate_user/', views.authenticate_user,
         name='authenticate_user'),
]
