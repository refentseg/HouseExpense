from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.contrib.auth.models import User


# Create your views here.
# Login User
def user_login(request):
    return render(request, 'authentication/login.html')


# Register User
def user_register(request):
    return render(request, 'authentication/register.html')


# Create User
def create_user(request):
    first_name = request.POST['first_name']
    username = request.POST['username']
    password = request.POST['password']
    password_confirm = request.POST['password_confirm']

    
    context = {}

    # Checks if user exists
    if User.objects.filter(username=username).exists():
        context['error'] = 'User already exists'
        return render(request, 'authentication/register.html', context)
    # Checks if passwords match
    if password != password_confirm:
        context['error'] = 'Passwords do not match'
        return render(request, 'authentication/register.html', context)
    # Creates user
    try:
        user = User.objects.create_user(first_name=first_name,
                                        username=username, password=password)
        user.save()

        # returns to login page
        return HttpResponseRedirect(
            reverse('user_auth:login')
        )
    except Exception as e:
        context['error'] = f"An error occurred: {str(e)}"
        return render(request, 'authentication/register.html', context)


# Authenticates user
def authenticate_user(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username=username, password=password)

    context = {}
    if user is None:
        context['error'] = "Username or password don't match. Please try again"
        return render(request, 'authentication/login.html', context)
    else:
        login(request, user)
        return HttpResponseRedirect(
            reverse('expense:index')
        )
