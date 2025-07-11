from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email Address")

class LoginForm(AuthenticationForm):
    username= forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Your username',
        'class':'w-full py-4 px-6 rounded-xl'
    }))
    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Your password',
        
    }))

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your username',
            'class': 'input-field',
        })
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your password',
            'class': 'input-field',
        })
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm your password',
            'class': 'input-field',
        })
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username
class UserProfileForm(forms.ModelForm):
    address = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your address', 'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
from .models import Profile
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address']