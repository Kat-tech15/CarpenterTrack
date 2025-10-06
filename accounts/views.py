from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model, logout, login, authenticate
from django.contrib import messages
from django.contrib.auth.models  import User
from .models import Contact

def home(request):

    return render(request, 'home.html')
    
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")
        
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, "Registration successful.")
        return redirect('login')  

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

def profile(request):
    profile = request.user.profile

    if request.method =="POST":
        profile.phone_number = request.POST.get("phone_number")
        profile.location = request.POST.get("location")

        if 'profile_image' in request.FILES:
            profile.profile_image = request.FILES['profile_image']
        
        profile.save()
        messages.success(request, "Profile updated successfully.")

    return render(request, 'accounts/profile.html', {"profile": profile})

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        Contact.objects.create(
            name=name,
            email=email,
            message=message
        )
        messages.success(request, "Message submitted successfully!")
        return redirect('contact')
    return render(request, 'accounts/contact.html')