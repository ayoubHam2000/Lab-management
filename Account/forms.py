from django import forms
from django.forms import ModelForm

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

from Utils.const import *
from Utils.functions import current_milli_time

from .models import MemberModel, DoctorantModel, UserAccount, EncadrantModel

#############################################
#Register
#############################################

class UserLogin(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)    

class AddMemberModelForm(ModelForm):
    def __init__(self, superAdmin = True, *args, **kwargs):
        super(AddMemberModelForm, self).__init__(*args, **kwargs)
        self.fields['userType'].label = "Type d'utilisateur"
        if not superAdmin:
            TYPES = (
                (ENCADRANT, 'ENCADRANT'),
                (DOCTORANT, 'DOCTORANT')
            )
            self.fields['userType'].choices = TYPES
        
    class Meta():
        model = MemberModel
        fields = [
            'email',
            'userType'
        ]

class CheckEmailForm(forms.Form):
    email = forms.CharField(max_length=MAXCHAR)
    def clean_email(self):
        email = self.cleaned_data.get('email')
        is_email_exist = MemberModel.objects.filter(email = email).exists()
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
    
    def userSetGroup(self, user, member):
        group = None
        if member.isAdmin():
            group = Group.objects.get(name = 'admin')
        elif member.isEncadrant():
            group = Group.objects.get(name = 'encadrant')
        elif member.isDoctorant():
            group = Group.objects.get(name = 'doctorant')
        user.groups.clear()
        user.groups.add(group)

    def saveUser(self, member):
        user = super(UserForm, self).save(commit=False)
        first_name = self.cleaned_data['first_name']

        user.email = member.email
        user.username = first_name + '_' + str(current_milli_time())
        user.save()

        self.userSetGroup(user, member)
        return user
    
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
    def __init__(self, readOnly = True, *args, **kwargs):
        super(DoctorantUpdateModelForm, self).__init__(*args, **kwargs)
        self.fields['these'].widget.attrs['readonly'] = readOnly

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