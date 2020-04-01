from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Profile
from django.contrib import messages
from django.core.mail import EmailMessage
# Create your views here.

def signup(request):
    if request.method == 'GET':
        return render(request, 'accounts/signup.html')
    else:
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        phone = request.POST['phone']
        try:
            is_owner = request.POST['is_owner'] == 'on'
        except:
            is_owner = False

        try:
            u = User.objects.get(email=email)
        except:
            u = None
        if u:
            messages.error(request, 'user already exist')
            return HttpResponseRedirect(reverse('signup'))
        else:
            if password1 == password2:
                user = User.objects.create_user(username, email, password1)
                user.save()
                profile = Profile(user=user, phonenumber=phone, is_owner=is_owner)
                profile.save()
                messages.success(request, f'thanks for signing up {user.username}')
                subject = f'{user.username} joined Renchant'
                message = f'''
                DETAILS OF {user.username}
                NAME : {user.username}
                EMAIL : {user.email}
                PHONE NUMBER : {user.profile.phonenumber}
                '''
                email_obj = EmailMessage(subject, message, '<EMAIL>', ['renchant@googlegroups.com',])
                return HttpResponseRedirect(reverse('login'))
            else:
                messages.error(request, 'passwords dont match')
                return HttpResponseRedirect(reverse('signup'))



def login_user(request):
    if request.method == 'POST':
        user_exist = False
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            user = authenticate(username=user.username, password=request.POST['password'])
            user_exist = True
        except:
            user = None

        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            if user.profile.is_owner:
                return HttpResponseRedirect(reverse('property_list'))
            else:
                if request.GET.get('next'):
                    pk = int(request.GET.get('property'))
                    return HttpResponseRedirect(reverse('details', args=(pk,)))
                return HttpResponseRedirect(reverse('about'))
        else:
            # No backend authenticated the credentials
            if user_exist:
                messages.error(request, 'incorrect password')
            else:
                messages.error(request, "user don't exist")
            return HttpResponseRedirect(reverse('login'))
    else:
        return render(request, 'accounts/login.html')

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))
