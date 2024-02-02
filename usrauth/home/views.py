from django.shortcuts import redirect, render

from django.contrib import messages
# --------- auth user model -----------
from django.contrib.auth.models import User

# ---- using the built in forms -------
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
# ---- for custom  forms ------
from . import forms

# ------- auth functions ---------
from django.contrib.auth import logout, authenticate, login
# to keep the user in session after password change
from django.contrib.auth import update_session_auth_hash

from django.contrib.auth.decorators import login_required

# Create your views here.
def index_page(request):
    messages.success(request, "Welcome")
    return render(request, 'index.html')

#----------------------------------------------------------------------------------------
# use of  login_required decorator:
#   - if the user is logged in, execute the view normally
#   - If the user isn't logged in, redirect to settings.LOGIN_URL
# The redirection occurs without message
#----------------------------------------------------------------------------------------
@login_required
def dash_page(request):
    return render(request, 'dashboard.html')

def login_user(request):
    if request.method == "POST":
        uname = request.POST["txtUName"]
        upass = request.POST["txtPass"]

        myuser = authenticate(username = uname, password = upass)
        if myuser is not None:
            login(request, myuser)
            messages.success(request, "Welcome ...")
            return redirect('/dash')
        else:
            messages.success(request, "Credential mismatch ..login again")
            return redirect('/signin')
    else:
        return render(request, 'authenticate/signin.html')


def logout_user(request):
    logout(request)
    messages.info(request, "Logout successful.")
    return redirect('/signin') #render(request, 'index.html')

#----------------------------------------------------------------------------------
#                   Basic registration form
#----------------------------------------------------------------------------------
def register_user(request):
    if request.method == "POST":
        myform = UserCreationForm(request.POST) # if the user has filled up a form & sumbitted then grab that object
        if myform.is_valid():  # validate the form
            myform.save()

            messages.success(request, "Registration successfull.")
            
            # registration complete ..now sign in, USE the cleaned_data() to get data from built-in forms
            uname = myform.cleaned_data['username']
            upass = myform.cleaned_data['password1']
            myuser = authenticate(username = uname, password = upass)
            login(request, myuser)
            return redirect('dashboard')
    else:
        myform = UserCreationForm()

    return render(request, 'authenticate/register_user.html', {'form' : myform})

#----------------------------------------------------------------------------------
#  Register with all fields (Custom registration form extended from UserCreationForm)
#----------------------------------------------------------------------------------
def register_user_all(request):
    if request.method == "POST":
        myform = forms.UserRegisterForm(request.POST) 
        if myform.is_valid():  # validate the form
            myform.save()

            messages.success(request, "Registration successfull")
            
            # registration complete ..now sign in
            """
            # * * * * * Get Form Data like request parameters use cleaned_data ******
            uname = myform.cleaned_data['username']
            upass = myform.cleaned_data['password1']
            myuser = authenticate(username = uname, password = upass)
            if myuser is not None:
                login(request, myuser)
                return redirect('dashboard')
            else:
                messages.error(request, "Credential mismatch ..login again")
                return redirect('signin')
            """
    # else:
    myform = forms.UserRegisterForm()

    return render(request, 'authenticate/register_user_all.html', {'form' : myform})

#----------------------------------------------------------------------------------
#                   Change password without authenticating old password
#----------------------------------------------------------------------------------
def changepass_user(request):
    if request.user.is_authenticated:
        current_user = request.user # * * * * * * * *

        print(current_user)

        if request.method == "POST":
            
            myform = forms.UpdatePasswordForm(current_user, request.POST)
            if myform.is_valid():
                myform.save()  # automatically logs out of the system
                messages.success(request, "Your password is updated. please login again")
                return redirect('signin')
                # --------- to persist the same session ------
                # update_session_auth_hash(request, myform.user)
                # return redirect('dashboard')
            else:
                #  * * * * * * * * error message handling * * * * * * * * * *
                for error in list(myform.errors.values()):
                    messages.warning(request, error)
                return redirect('change-pass')
                
        else:
            myform = forms.UpdatePasswordForm(current_user)
            return render(request, 'authenticate/change_pwd.html', {'pform' : myform})        
    
    else:
        messages.warning(request, "Please sign in to access this page")
        return redirect('signin')

#----------------------------------------------------------------------------------
#             Change password with authentication of old password
#----------------------------------------------------------------------------------
@login_required
def changepass_withauth(request):
    myform = PasswordChangeForm(user=request.user, data=request.POST or None)

    if myform.is_valid():
        myform.save()
        # * * * * * * update the session after changing password so that the user isn't logged off. * * * * * 
        update_session_auth_hash(request, myform.user)

        messages.info(request, "Hoorrrayyyy !! Your password has changed")
        return redirect('change-pass-auth')
    
    return render(request, 'authenticate/change_pwd.html', {'pform' : myform})

#----------------------------------------------------------------------------------
#                   Update profile
#----------------------------------------------------------------------------------
def update_profile(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id = request.user.id)

        user_form = forms.UpdateProfileForm(request.POST or None, instance = current_user)

        if user_form.is_valid():  # validate the form
            user_form.save()

            messages.success(request, "Profile details saved successfull")
            return redirect('dashboard')

        return render(request, 'authenticate/profile.html', {'user_form' : user_form})
    else:
        messages.warning(request, "Please sign in to access this page")
        return redirect('home')
    
