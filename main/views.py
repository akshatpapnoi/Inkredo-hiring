from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserForm, UserProfileForm, CompanyForm
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Company
# Create your views here.


def home(request):
	return HttpResponseRedirect(reverse('main:login'))

def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('main:dashboard'))
    elif request.method == 'POST':
        user_form = UserCreationForm(data=request.POST)
        user_profile_form = UserProfileForm(data=request.POST)
  
        if user_form.is_valid() and user_profile_form.is_valid():
            user = user_form.save()
            #user.set_password(user.password)
            
            profile = user_profile_form.save(commit=False)
            profile.user = user
            profile.save()

            return HttpResponseRedirect(reverse('main:login'))

        else:
            messages.error(request, 'Password and confirm password does not match!')
            return HttpResponseRedirect(reverse('main:dashboard'))

    else:
    	user_form = UserCreationForm()
    	user_profile_form = UserProfileForm()
    	return render(request, 'register.html', {'user_form':user_form, 'user_profile_form': user_profile_form})

def user_login(request):
    if request.method == 'POST':
        if UserProfile.objects.filter(user__username = request.POST['username']).exists():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
            	login(request, user)
            	return HttpResponseRedirect(reverse('main:dashboard'))
    		 
        else:
        	messages.error(request, 'Invalid credentials. Try again.')
        	return HttpResponseRedirect(reverse('main:login'))
    else:
    	if request.user.is_authenticated:
    		return HttpResponseRedirect(reverse('main:dashboard'))
    	else:
    		return render(request, 'login.html', {})



@login_required(login_url=reverse_lazy('main:login'))
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('main:login'))

@login_required(login_url=reverse_lazy('main:login'))
def dashboard(request):
    user = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        userProfile = UserProfileForm(data=request.POST, instance=user)
        if userProfile.is_valid():
            userProfile.save()
            return HttpResponseRedirect(reverse('main:dashboard'))
        else:
            return HttpResponse('INVALID FORM')

    else:
        userProfile = UserProfileForm(instance=user)
        return render(request, 'dashboard.html', {'form': userProfile, 'name' : user.name })

def company_register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('main:dashboard'))
    elif request.method == 'POST':
        user_form = UserCreationForm(data=request.POST)
        company_form = CompanyForm(data=request.POST)
  
        if user_form.is_valid() and company_form.is_valid():
            user = user_form.save()
            #user.set_password(user.password)
            
            company = company_form.save(commit=False)
            company.admin = user
            company.save()

            return HttpResponseRedirect(reverse('main:company-login'))

        else:
            messages.error(request, 'Password and confirm password does not match!')
            return HttpResponseRedirect(reverse('main:company-register'))

    else:
        user_form = UserCreationForm()
        company_form = CompanyForm()
        return render(request, 'company-register.html', {'user_form':user_form, 'company_form': company_form})

def company_login(request):
    if request.method == 'POST':
        if Company.objects.filter(admin__username = request.POST['username']).exists():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('main:company-dashboard'))
             
        else:
            messages.error(request, 'Invalid credentials. Try again.')
            return HttpResponseRedirect(reverse('main:company-login'))

    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('main:company-dashboard'))
        else:
            return render(request, 'company-login.html', {})

def company_dashboard(request):
    company = Company.objects.get(admin=request.user)
    employees = UserProfile.objects.filter(company=company)

    return render(request, 'company-dashboard.html', {'employees':employees, 'company':company})
