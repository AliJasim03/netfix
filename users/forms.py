from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, authenticate
from django.db import transaction
from django.core.exceptions import ValidationError

from .models import User, Company, Customer


class DateInput(forms.DateInput):
    input_type = 'date'


def validate_email(value):
    # In case the email already exists in an email input in a registration form, this function is fired
    if User.objects.filter(email=value).exists():
        raise ValidationError(
            value + " is already taken.")


class CustomerSignUpForm(UserCreationForm):
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter Email'
        })
    )
    date_of_birth = forms.DateField(
        required=False,
        widget=DateInput(attrs={
            'placeholder': 'Enter your birthdate (DD/MM/YYYY)'
        })
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter Password'
        }),
        help_text=UserCreationForm().fields['password1'].help_text  # Retain the default help text
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm Password'
        }),
        help_text=UserCreationForm().fields['password2'].help_text  # Retain the default help text
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Enter Username'
            }),

        }

        
    @transaction.atomic
    def save(self, commit=True):
        # Save the User model first
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')  # Set the email manually
        user.is_customer = True  # Mark the user as a customer
        if commit:
            user.save()  # Save the user instance
            
            # Create the Customer instance and link it to the user
            Customer.objects.create(
                user=user,
                date_of_birth=self.cleaned_data.get('date_of_birth')
            )
        return user


class CompanySignUpForm(UserCreationForm):
    pass


class UserLoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter Email'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['autocomplete'] = 'off'
