from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import AppUser, UserType

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = AppUser 
        fields = ['username', 'email'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=255, required=True)
    user_type = forms.ChoiceField(
        choices=UserType.choices,  
        widget=forms.Select(attrs={
            'class': 'form-select',  
        }),
        label="Tipo de Usuario"
    )
    class Meta:
        model = User
        fields = ('username','email','password1','password2','user_type')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user