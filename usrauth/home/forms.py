from typing import Any
from django import forms
# ---- built in forms-----
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm, PasswordChangeForm

from django.contrib.auth.models import User

# =======================================================================================
#           Custom SignUp Model with all the fields in table
# extends the properties of UserCreationForm which has only username, password1 & password2
# =======================================================================================
class UserRegisterForm(UserCreationForm):
    """
    widgets are optional parameters for making the form lukrative like bootstrap
    https://docs.djangoproject.com/en/5.0/ref/forms/widgets/
    """
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder' : 'something@django.com'}))
    first_name = forms.CharField(max_length=50, 
                                 widget=forms.TextInput(attrs={'class': 'form-control' }))
    last_name = forms.CharField(max_length=50, 
                                widget=forms.TextInput(attrs={'class': 'form-control' }))

    class Meta:  
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

        

    # following is required to decorate the 3 default fiels of UserCreationForm e.g. username, password1 & password2

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Your username'
        self.fields['username'].label = 'User_name'
        self.fields['username'].help_text = "<span class='form-text text-muted'><small>Required. maximum 50 characters allowed with letter, digits and @/./+/-/_<small><span>"

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

        # NO NEED TO USE OPTIONAL  widgets & custom labels for form fields xxxx ===>>>>> Wont work for UserCreationForm children
        

# =======================================================================================
#           Custom Change profile details model 
#   Note: it does not allow you to change password
# =======================================================================================
class UpdateProfileForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder' : 'something@example.com'}))
    first_name = forms.CharField(max_length=50, 
                                 widget=forms.TextInput(attrs={'class': 'form-control' }))
    last_name = forms.CharField(max_length=50, 
                                widget=forms.TextInput(attrs={'class': 'form-control' }))
    
    # HIDE password related warning
    password = None

    class Meta:  
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')  # password removed

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Your username'
        self.fields['username'].label = 'User_name'
        self.fields['username'].help_text = "<span class='form-text text-muted'><small>Required. maximum 50 characters allowed with letter, digits and @/./+/-/_<small><span>"

# =======================================================================================
#           Custom Change password model without authenticating old password
#           This form is just for MAKEUP purpose, you can directly use SetPasswordForm() from the view function
# =======================================================================================
class UpdatePasswordForm(SetPasswordForm):
    class Meta:  
        model = User
        fields = ('new_password1', 'new_password2') 
    
    def __init__(self, *args, **kwargs):
        super(UpdatePasswordForm, self).__init__(*args, **kwargs)

        self.fields['new_password1'].widget.attrs['class'] = 'form-control'

        self.fields['new_password2'].widget.attrs['class'] = 'form-control'

