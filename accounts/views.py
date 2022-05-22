from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail


#this function will send the mail from email_host_user  to the registered id and inthat mail from
#there is token that will be used  to verify the given account.
def send_mail_after_registration( email, token):
    subject = 'verification mail from meta'
    message = f'Hi!, thanks a lot for spending your time in meta. click on the following link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )



# Create your views here.
def home(request):
    return render(request, 'login.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
    return render(request, 'login.html')


def send_mail_for_reset_password( username, email, token):
    subject = 'Mail for reseting your password'
    message = f'Hi {username}!, you have requested a reset password link, so click on the  given link for reseting your password http://127.0.0.1:8000/reset_verify/{token}. Do not share with anyone else.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )
    
    
    
    
    
    
    
def reset_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user_obj = User.objects.get(username=username)
            if user_obj:
                email = user_obj.email
                auth_token=user_obj.auth_token
                send_mail_for_reset_password(username, email, auth_token)
                messages.success(request, 'reset password is sent your regisered email address')
                
            else:
                return redirect('/reset_error')
        except Exception as e:
            print(e)
    return render(request, 'reset.html')

def reset_verify(request, auth_token):
    if request.method == 'POST':
        password = request.POST.get('password')
        profile_obj=Profile.objects.filter(auth_token=auth_token).first()
        user_obj=profile_obj.user
        pass
        
    
    
    return render(request, 'reset_verify.html')
        
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email=request.POST.get('email')
        password = request.POST.get('password')
        try:
            if User.objects.filter(username=username).first():
                messages.info(request,'This Username is already taken, choose another username')
                return redirect('/register')
            if User.objects.filter(email=email).first():
                messages.info(request,'This email is already registered, choose another email')
                return redirect('/register')
            
            
            user_obj = User.objects.create(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token= str(uuid.uuid4())
            profile_obj = Profile.objects.create(user=user_obj,auth_token=auth_token)
            profile_obj.save()
            send_mail_after_registration(email, auth_token)
            return redirect('/token_send')
        except Exception as e:
            print(e)
    return render(request, 'register.html')


#verification function; this func will be called by the clicking the link which is send to registered mail of that person

def verify(request, auth_token):
    try:
        profile_obj=Profile.objects.filter(auth_token=auth_token).first() #checking if that profile is exist or not with that auth token
        if profile_obj.is_verified:
            messages.success(request, 'congrats! your email is already verified')
            return redirect('/')
            
        else:
            if profile_obj:
                profile_obj.is_verified=True
                profile_obj.save()
                messages.success(request, 'congrats! your email has been verified')
                return redirect('/success')
            else:
                return redirect('/error')
    except Exception as e:
        print(e)


def error(request):     #error page if email is not verified
    return render(request, 'error.html')

def success(request):
    return render(request, 'success.html')

def token_send(request):
    return render(request, 'token_send.html')


      