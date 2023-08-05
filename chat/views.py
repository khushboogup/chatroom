from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Message  
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q 
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout
 
def home(request):
    if not request.user.is_authenticated:
        return redirect("login")    
    messages=Message.objects.all().order_by('-created_at')
    return render(request,'base/home.html',{'messages':messages})
def post_message(request):
    if request.method=='POST' and request.user.is_authenticated:
        content=request.POST.get('content','')
        if content.strip():
            Message.objects.create(user=request.user,content=content)
    return redirect("home")
def user_login(request):
    if request.method=='POST':
        form=AuthenticationForm(request,request.POST)
        if form.is_valid():
            login(request,form.get_user())
            return redirect('home')
    else:
        form=AuthenticationForm()
    return render(request,'base/login.html',{'form':form})

def user_logout(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form=UserCreationForm()
    return render (request,'base/register.html',{'form':form})
            
