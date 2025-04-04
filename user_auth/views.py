from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.contrib.auth.models import User


# Create your views here.
# Login User
def user_login(request):
    # Display login page to user
    return render(request, 'authentication/login.html')


# Register User
def user_register(request):
    # Display register page to user
    return render(request, 'authentication/register.html')


# Create User
def create_user(request):
    # Get user input from registration form
    # Extract form data from the POST request
    first_name = request.POST['first_name']
    username = request.POST['username']
    password = request.POST['password']
    password_confirm = request.POST['password_confirm']

    # Initialize empty context dictionary to store response data
    # Used to display error message/s back to user
    context = {}

    # Checks if user exists
    if User.objects.filter(username=username).exists():
        # Add error message to context
        context['error'] = 'User already exists'
        # Display registration form
        return render(request, 'authentication/register.html', context)
    # Checks if passwords match
    if password != password_confirm:
        # Add error message to context
        context['error'] = 'Passwords do not match'
        # Display registration form
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
        # Add error message to context
        context['error'] = f"An error occurred: {str(e)}"
        # Re-render registration page
        return render(request, 'authentication/register.html', context)


# Authenticates user
def authenticate_user(request):
    # Get user input from loginn form
    # Extract form data from the POST request
    username = request.POST['username']
    password = request.POST['password']

    # Verify user's credentials
    user = authenticate(username=username, password=password)

    # Initialize empty context dictionary to store response data
    # Used to display error message/s back to user
    context = {}

    # Checks if authentication failed
    if user is None:
        # Add error message to context
        context['error'] = "Username or password don't match. Please try again"
        # Re-render login page
        return render(request, 'authentication/login.html', context)
    else:
        # Authentication was successful, and logs in user
        login(request, user)
        # Redirect user to homepage
        return HttpResponseRedirect(
            reverse('expense:index')
        )
