from django import forms
from django.forms import ModelForm
from django.db.models import Q

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

from Utils.const import *
from Utils.functions import current_milli_time

from .models import (
    UserAccount, 
    DoctorantModel, 
    EncadrantModel, 
    RelationModel,
)

#############################################
#Register
#############################################

class UserLogin(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)    

class AddUserForm(forms.Form):
    TYPES = (
        (ENCADRANT, 'ENCADRANT'),
        (DOCTORANT, 'DOCTORANT'),
        (ADMIN, 'ADMIN'),
    )
    email = forms.EmailField()
    userType = forms.ChoiceField(choices= TYPES)
    
    def __init__(self, user, *args, **kwargs):
        super(AddUserForm, self).__init__(*args, **kwargs)
        self.fields['userType'].label = "Type d'utilisateur"
        if not user.isSuperAdmin():
            TYPES = (
                (ENCADRANT, 'ENCADRANT'),
                (DOCTORANT, 'DOCTORANT')
            )
            self.fields['userType'].choices = TYPES
    
    def save(self):
        email = self.cleaned_data['email']
        group = self.cleaned_data['userType']
        UserAccount.objects.create_user(email = email, group=group,password='123456789')

class CheckEmailForm(forms.Form):
    email = forms.CharField(max_length=MAXCHAR)
    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        is_email_exist = UserAccount.objects.filter(email = email).exists()
        if not is_email_exist:
            raise forms.ValidationError("cet e-mail n'a pas encore été ajouté")
        return email

#############################################

class UserForm(UserCreationForm):
    class Meta:
        model = UserAccount
        fields = [
            'first_name',
            'last_name',
            'password1',
            'password2'
        ]
        labels = {
            "first_name": "Prénom",
            "last_name": "Nom",
        }
    
class DoctorantModelForm(ModelForm):
    class Meta:
        model = DoctorantModel
        fields = [
            'university',
            'apogee',
            'cin',
        ]
        labels = {
            "university": "Université"
        }
    def saveDoctorant(self, user):
        doctorant = super(DoctorantModelForm, self).save(commit=False)
        doctorant.user = user
        doctorant.save()
        return doctorant

class EncadrantModelForm(ModelForm):
    class Meta:
        model = EncadrantModel
        fields = [
            'university'
        ]
        labels = {
            "university": "Université"
        }
    def saveEncadrant(self, user):
        encadrant = super(EncadrantModelForm, self).save(commit=False)
        encadrant.user = user
        encadrant.save()
        return encadrant

#############################################
#Update
#############################################
class UserUpdateForm(ModelForm):
    profile_image = forms.ImageField(
        label='Profile Image',
        required=False, 
        error_messages = {'invalid':"Fichiers image uniquement"}, 
        widget=forms.FileInput)

    class Meta:
        model = UserAccount
        fields = [
            'profile_image',
            'first_name',
            'last_name',
        ]
        labels = {
            "first_name": "Prénom",
            "last_name": "Nom",
        }

class DoctorantUpdateModelForm(ModelForm):    
    def __init__(self, user, targetUser, *args, **kwargs):
        assert isinstance(user, UserAccount)
        assert isinstance(targetUser, UserAccount)
        super(DoctorantUpdateModelForm, self).__init__(*args, **kwargs)
        is_my_doctorant = RelationModel.getEncadrant(targetUser) == user
        if not (user.isAdmin() or is_my_doctorant):
            self.fields['these'].widget.attrs['readonly'] = True

    these = forms.TextInput(attrs={'readonly':'readonly'})
    class Meta:
        model = DoctorantModel
        fields = [
            'university',
            'apogee',
            'cin',
            'these'
        ]
        labels = {
            "university": "Université"
        }

class EncadrantUpdateModelForm(ModelForm):
    class Meta:
        model = EncadrantModel
        fields = [
            'university'
        ]
        labels = {
            "university": "Université"
        }
        
class UpdatePasswordModelFrom(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=True)     
    class Meta:
        model = UserAccount
        fields = [
            'password'
        ]