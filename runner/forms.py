from django.forms import ModelForm
from django import forms
from .models import *


class RunoneForm(ModelForm):
    class Meta:
        model = Runone
        fields = ('name', 'image', 'description',)



class RunoneUploadForm(ModelForm):
    class Meta:
        model = Upload
        fields = ('image',)


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class SearchForm(forms.Form):
    query = forms.CharField()


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
