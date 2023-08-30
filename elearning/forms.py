from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Room, ForalUser


class MyusercreationForm(UserCreationForm):
    class Meta:
        model = ForalUser
        fields = ['name', 'username', 'email', 'password1', 'password2', 'Bio']

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude =['hostname', 'participant']


class Userform(forms.ModelForm):
    class Meta:
        model = ForalUser
        fields = ['avatar', 'name', 'email', 'Bio']
