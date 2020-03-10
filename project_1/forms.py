from django import forms
from . import models


class MaterialForm(forms.ModelForm):
    class Meta:
        model = models.NewsGame
        fields = ('title', 'body', 'status')


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ('name', 'email', 'body')
