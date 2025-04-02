from django.urls import path

from user_auth import views

app_name = 'user_auth'
urlpatterns = [
    path('', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('create_user/', views.create_user, name='create_user'),
    path('authenticate_user/', views.authenticate_user,
         name='authenticate_user'),
]
