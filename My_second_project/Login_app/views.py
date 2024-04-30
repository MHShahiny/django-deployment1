from django.shortcuts import render
from Login_app.form import UserForm, UserInfoForm
from Login_app.models import Userinfo
from django.contrib.auth.models import User



from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from django.urls import reverse

def login_page(request):
    return render(request, 'Login_app/login.html', {})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('Login_app:index'))  # Corrected 'index' URL name
            else:
                return HttpResponse("Your account is inactive.")
        else:
            return HttpResponse('Login details are wrong')
    else:
        return render(request, 'Login_app:login', context={})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('Login_app:index'))



@login_required
@login_required
def index(request):
    user_basic_info = None
    user_more_info = None
    
    if request.user.is_authenticated:  # Removed unnecessary parentheses ()
        current_user = request.user
        try:
            user_basic_info = User.objects.get(pk=current_user.id)
            user_more_info = Userinfo.objects.get(user=current_user)
        except User.DoesNotExist:
            pass  # Handle the case where user_basic_info is not found
        except Userinfo.DoesNotExist:
            pass  # Handle the case where user_more_info is not found
    
    context = {'user_basic_info': user_basic_info, 'user_more_info': user_more_info}
    return render(request, 'Login_app/index.html', context=context)

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        user_info_form = UserInfoForm(data=request.POST)
        if user_form.is_valid() and user_info_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            user_info = user_info_form.save(commit=False)
            user_info.user = user
            if 'profile_pic' in request.FILES:
                user_info.profile_pic = request.FILES['profile_pic']
            user_info.save()
            registered = True
    else:
        user_form = UserForm()
        user_info_form = UserInfoForm()

    context = {'user_form': user_form, 'user_info_form': user_info_form, 'registered': registered}
    return render(request, 'Login_app/register.html', context=context)  # Corrected template path
