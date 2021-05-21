from django import forms
from django.forms import ModelForm

from Utils.const import *
from Utils.functions import current_milli_time

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

from .models import MemberModel, DoctorantModel, UserAccount, EncadrantModel


class UserLogin(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)    

class AddMemberModelForm(ModelForm):
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

class DoctorantForm(UserCreationForm):
    member = None

    university = forms.ChoiceField(choices = UNIVERSITIES)
    apogee = forms.CharField(max_length=APOGEE_MAX, min_length=APOGEE_MAX)
    cin = forms.CharField(max_length=CIN_MAX, min_length=CIN_MAX)
    class Meta:
        model = UserAccount
        fields = [
            'first_name',
            'last_name',
            'password1',
            'password2'
        ]
    
    def customSave(self, member):
        self.member = member
        user = self.save()

        doctorant = DoctorantModel.objects.create(
            user = user,
            university = self.cleaned_data['university'] ,
            apogee = self.cleaned_data['apogee'],
            cin = self.cleaned_data['cin']
        )

        group = Group.objects.get(name = 'doctorant')

        user.groups.add(group)

        doctorant.save()
        member.signed = True
        member.save()

    def save(self, commit=True):
        first_name = self.cleaned_data['first_name']

        user = super(DoctorantForm, self).save(commit=False)
        user.email = self.member.email
        user.user_type = self.member.userType
        user.username = first_name + '_' + str(current_milli_time())
        if commit:
            user.save()
        return user

class EncadrantForm(UserCreationForm):
    member = None

    university = forms.ChoiceField(choices = UNIVERSITIES)
    class Meta:
        model = UserAccount
        fields = [
            'first_name',
            'last_name',
            'password1',
            'password2'
        ]
    
    def customSave(self, member):
        self.member = member
        user = self.save()

        encadrant = EncadrantModel.objects.create(
            user = user,
            university = self.cleaned_data['university']
        )

        group = Group.objects.get(name = 'encadrant')

        user.groups.add(group)

        encadrant.save()
        member.signed = True
        member.save()

    def save(self, commit=True):
        first_name = self.cleaned_data['first_name']

        user = super(EncadrantForm, self).save(commit=False)
        user.email = self.member.email
        user.user_type = self.member.userType
        user.username = first_name + '_' + str(current_milli_time())
        if commit:
            user.save()
        return user


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
    
    def userSetGroup(self, user, member):
        group = None
        if member.userType == MemberModel.DOCTORANT:
            group = Group.objects.get(name = 'doctorant')
        if member.userType == MemberModel.ENCADRANT:
            group = Group.objects.get(name = 'encadrant')
        user.groups.clear()
        user.groups.add(group)

    def saveUser(self, member):
        user = super(UserForm, self).save(commit=False)
        first_name = self.cleaned_data['first_name']

        user.email = member.email
        user.user_type = member.userType
        user.username = first_name + '_' + str(current_milli_time())
        user.save()

        self.userSetGroup(user, member)
        return user
    
    def updateUser(self, member):
        user = super(UserForm, self).save(commit=False)
        user.user_type = member.userType
        user.save()

        self.userSetGroup(user, member)
        return user


class DoctorantModelForm(ModelForm):
    university = forms.ChoiceField(choices = UNIVERSITIES)
    class Meta:
        model = DoctorantModel
        fields = [
            'university',
            'apogee',
            'cin',
        ]
    def saveDoctorant(self, user):
        doctorant = super(DoctorantModelForm, self).save(commit=False)
        doctorant.user = user
        doctorant.save()
        return doctorant

class EncadrantModelForm(ModelForm):
    university = forms.ChoiceField(choices = UNIVERSITIES)
    class Meta:
        model = EncadrantModel
        fields = [
            'university'
        ]
    def saveEncadrant(self, user):
        encadrant = super(EncadrantModelForm, self).save(commit=False)
        encadrant.user = user
        encadrant.save()
        return encadrant