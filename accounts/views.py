from django.shortcuts import redirect, render
from accounts.utils import detectUser

from vendor.forms import VendorForm
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
# Create your views here.

#restrict vendor from accessing customer pages
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied


#restrict customer from accessing vendor pages
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in.')
        return redirect('dashboard')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():

            #2 ways of creating user

            # Create user using form
            # password = form.cleaned_data['password']
            # user = form.save(commit=False)
            # user.set_password(password)
            # user.role = User.CUSTOMER
            # user.save()

            #Create user with create_user method in models.py
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name = first_name, last_name=last_name, username = username, email=email, password=password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, 'Your account has been registered successfully')
            return redirect('registerUser')
        else :
            print('form is invalid')
            print(form.errors)
    else:
        form = UserForm
    context = {
        'form': form
    }
    return render(request, 'accounts/registerUser.html', context)


def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in.')
        return redirect('dashboard')
    elif request.method == 'POST':
        #store the data and create vendor account
        form = UserForm(request.POST)
        vendor_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and vendor_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name = first_name, last_name=last_name, username = username, email=email, password=password)
            user.role = User.VENDOR
            user.save()
            vendor = vendor_form.save(commit=False)
            vendor.user = user
            user_profile= UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, 'Your account has been registered successfully ! Please wait for the approval')
            return redirect('registerVendor')
        else:
            print('invalid form')
            print(form.errors)
    form = UserForm()
    vendor_form = VendorForm()
    context = {
        'form': form,
        'vendor_form':vendor_form
    }
    return render(request, 'accounts/registerVendor.html', context)


def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in.')
        return redirect('myAccount')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password = password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('myAccount')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request, 'You are logged out')
    return redirect('login')

@login_required(login_url='login') #if not logged in,user will be redirected to login url 
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url='login') #if not logged in,user will be redirected to login url 
@user_passes_test(check_role_customer)
def customerDashboard(request):
    return render(request, 'accounts/customerDashboard.html')

@login_required(login_url='login') #if not logged in,user will be redirected to login url 
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request, 'accounts/vendorDashboard.html')