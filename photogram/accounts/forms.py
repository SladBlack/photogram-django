from django import forms
from django.contrib.auth.models import User


class UpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']


class CreateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
