# your_app/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordResetForm as BasePasswordResetForm
from django.contrib.auth import get_user_model
from .models import DiaryEntry, CustomUser


class DiaryEntryForm(forms.ModelForm):
    class Meta:
        model = DiaryEntry
        fields = ['title', 'content']

    def save(self, user, commit=True):
        instance = super().save(commit=False)
        instance.user = user
        if commit:
            instance.save()
        return instance


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.',
                             error_messages={
                                 'invalid': 'Please enter a valid email address.',
                             }
                             )

    password1 = forms.CharField(label="Password",
                                strip=False,
                                widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
                                error_messages={
                                    'min_length': 'Password must be at least 8 characters long.',
                                    'password_too_common': 'This password is too common.',
                                }
                                )

    password2 = forms.CharField(label="Confirm Password",
                                strip=False,
                                widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
                                error_messages={
                                    'password_mismatch': "The passwords do not match.",
                                }
                                )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def clean_password2(self):
        # Check if the passwords match
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match.")
        return password2


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class PasswordResetForm(BasePasswordResetForm):
    email = forms.EmailField(
        label='Email',
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'}),
    )

    def get_users(self, email):
        """
        Given an email, return matching user(s) who should receive a reset.
        This is overridden to use your CustomUser model.
        """
        active_users = get_user_model()._default_manager.filter(
            email__iexact=email,
            is_active=True,
        )
        return (u for u in active_users if u.has_usable_password() and u.is_active)



class NewPasswordResetForm(forms.Form):
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput,
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput,
    )