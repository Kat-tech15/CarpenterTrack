from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model, logout, login, authenticate
from django.contrib import messages
from .models import CustomUser


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')
        
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")
        
        user = CustomUser.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, "Registration successful.")
        return redirect('login')  # Redirect to a home page or dashboard after registration
    return render(request, 'accounts/register.html')

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect("home")
        else:
            messages.error(request, "Invalid email or password.")
            return redirect("login")
        
    return render(request, 'accounts/login.html')


def logout(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return render(request, 'accounts/logout.html')



