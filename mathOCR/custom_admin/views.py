from django.shortcuts import render
from app.models import User, Images, RecognitionResults
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count
from django.shortcuts import redirect
from datetime import datetime, timedelta
from django.db.models.functions import ExtractDay, ExtractMonth, ExtractYear, ExtractHour
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.contrib import messages



# Create your views here.

def admin_login(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect("dashboard")
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user_obj = User.objects.filter(username=username)
        if not user_obj.exists():
            return render(request, "login.html", {"error": "User not found"})
        
        user_obj = authenticate(username=username, password=password)
        if user_obj and user_obj.is_superuser:
            login(request, user_obj)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid password or user is not admin")
        
        return render(request, "login.html", {"error": "Invalid password"})
    return render(request, "login.html")
        
def admin_logout(request):
    logout(request)
    return redirect("login-admin")

def admin_edit(request, pk):
    if not request.user.is_authenticated:
        return redirect("login-admin")
    
    user = User.objects.get(pk=pk)
    if request.method == "POST":
        user.username = request.POST["username"]
        user.email = request.POST["email"]
        user.set_password(request.POST["password"])
        user.raw_password = request.POST["password"]
        user.save()
        return redirect("dashboard")
    
    context = {
        "user": user
    }
    return render(request, "edit.html", context)

def admin_delete(request, pk):
    if not request.user.is_authenticated:
        return redirect("login-admin")
    
    user = User.objects.get(pk=pk)
    user.delete()
    return redirect("dashboard")

def admin_signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        user = User.objects.create_user(username=username, email=email, password=password)
        user.raw_password = password
        user.is_superuser = True
        user.save()
        return redirect("dashboard")
    
    return render(request, "signup.html")

def index(request):
    if not request.user.is_authenticated:
        return redirect("login-admin")
    
    users = User.objects.all()

    recognition_requests = (
        RecognitionResults.objects
        .filter(timestamp__gte=timezone.now() - timedelta(days=1))
        .annotate(year=ExtractYear('timestamp'), month=ExtractMonth('timestamp'), day=ExtractDay('timestamp'), hour=ExtractHour('timestamp'))
        .values('year', 'month', 'day', 'hour')
        .annotate(result_count=Count('resultID'))
        .order_by('year', 'month', 'day', 'hour')
    )
    image_results = Images.objects.annotate(result_count=Count('recognition_results'))

    context = {
        "users": users,
        "recognition_requests": recognition_requests,
        "image_results": image_results
    }
    return render(request, "dashboard.html", context)
