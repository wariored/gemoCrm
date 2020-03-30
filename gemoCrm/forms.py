from django.contrib.auth.models import User
from django import forms
from secrets import compare_digest


class UserProfileForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    repeat_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']

    def clean(self):
        password = self.cleaned_data['password']
        repeat_password = self.cleaned_data['repeat_password']
        if not compare_digest(password, repeat_password):
            self.add_error('repeat_password', 'passwords does not match')
        return self.cleaned_data

    def save(self, commit=True):
        password = self.cleaned_data['password']
        self.instance.set_password(password)
        return super().save(commit)
