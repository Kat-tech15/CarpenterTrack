from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import logout, login, authenticate, get_user_model
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models  import User
from django.core.mail import send_mail
from django.http import HttpResponse
from .models import Contact
from products.models import Product
from django.utils import timezone
from datetime import datetime
import os

def home(request):

    featured_products = Product.objects.all()[:8]

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
        return redirect('home')
    return render(request, 'home.html', {'featured_products': featured_products, 'year': datetime.now().year})
    
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password1 = request.POST.get("password1")

        
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Registration successful.")
        return redirect('login_view')  

    return render(request, 'accounts/register.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("login_view")
        
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return render(request, 'accounts/logout.html')

def profile(request):
    profile = request.user.profile

    if request.method =="POST":
        profile.phone_number = request.POST.get("phone")
        profile.location = request.POST.get("location")
        profile.bio = request.POST.get('bio')

        if 'profile_image' in request.FILES:
            profile.profile_image = request.FILES['profile_image']
        
        profile.save()
        messages.success(request, "Profile updated successfully.")

    return render(request, 'accounts/profile.html', {"profile": profile})

@staff_member_required
def admin_messages(request):
    message_list = Contact.objects.all().order_by('-created_at')
    return render(request, 'accounts/admin_messages.html', {'contact_list': message_list})

@staff_member_required
def reply_message(request, message_id):
    msg = get_object_or_404(Contact, id=message_id)
    if request.method == 'POST':
        response_text = request.POST.get('response')
        msg.response =  response_text
        msg.responded_at = timezone.now()
        msg.is_read = True
        msg.save()

        send_mail(
            subject='Response to your message on CarpenterTrack',
            message=f"Hello {msg.name}, \n\nAdmin has responded to your message:\n\n{response_text}\n\nThank you. ",
            from_email=os.getenv('EMAIL_HOST_USER'),
            recipient_list=[msg.email],
            fail_silently=False
        )
        messages.success(request, "Message responded to successfully and email send to the user!")
        return redirect('admin_messages')
    return render(request, 'accounts/respond_message.html', {'message': msg})

@staff_member_required
def delete_message(request, message_id):
    msg = get_object_or_404(Contact, id=message_id)
    msg.delete()
    messages.success(request, "Message deleted successfully!")
    return redirect('admin_messages')  

def create_superuser(request):
    User = get_user_model()
    username = 'admin'  
    email = 'kelvinmutua269@gmail.com'
    password = 'cekret'

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        return HttpResponse("superuser created successfully!")
    return HttpResponse("Superuser already exists!")
    