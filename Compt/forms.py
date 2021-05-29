from django import forms
from django.forms import ModelForm

from .models import PostModel


class PostModelForm(forms.ModelForm):
    class Meta():
        model = PostModel
        fields = '__all__'
        exclude = ['user']

    def __init__(self, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PostModelForm, self).__init__(**kwargs)

    def save(self, commit=True):
        obj = super(PostModelForm, self).save(commit=False)
        obj.user = self.user
        if commit:
            obj.save()
        return obj

