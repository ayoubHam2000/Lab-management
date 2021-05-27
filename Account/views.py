#region import
from django.shortcuts import render,HttpResponse
from django.urls import reverse
from django.views import View
from django.contrib.auth.models import Group
from django.http import HttpResponseBadRequest


from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

#Custom
from .authenticate import unauthenticated_user, allowed_users, dedicated
from Utils.functions import myredirect, current_milli_time
from Utils.const import *


from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
#endregion

#region froms and models
from .forms import (
    AddMemberModelForm,
    UserLogin,
    CheckEmailForm,

    DoctorantForm,
    EncadrantForm,

    DoctorantModelForm,
    UserForm,
    EncadrantModelForm
)

from .models import (
    MemberModel,
    DoctorantModel,
    EncadrantModel,
    UserAccount,
)
#endregion

#region decorator

decorator_login = [login_required(login_url='/login/')]
decorator_auth = [unauthenticated_user]
decorator_dedicated = [dedicated]
def decorator_user(allowed_roles):
    return [allowed_users(allowed_roles=allowed_roles)]

#endregion

#region Register


class TestView(View):
    #template_name = 'Registration/test.html'

    def get(self, request):
        return myredirect('Account:login')
        #context = {}
        #return render(request, self.template_name, context)

# if already log in go to home page
@method_decorator(decorator_auth, name = 'dispatch')
class LoginView(View):
    template_name = 'Registration/login.html'

    def get(self, request):
        form = UserLogin()
        context = {
            "form" : form
        }
        return render(request, self.template_name, context)

    def checkMemberValide(self, email):
        member = MemberModel.objects.filter(email = email)
        if not member.exists():
            return False
        return member[0].active
            

    def post(self, request):
        form = UserLogin()
        email = request.POST.get('email')
        password = request.POST.get('password')

        
        user = authenticate(request, email = email, password = password)

        if user is not None:
            isAdmin = user.groups.all()[0].name == 'admin'
            if not self.checkMemberValide(email) and not isAdmin:
                messages.info(request, 'votre compte a eté retirer ')
            else:
                login(request, user)
                return myredirect( 'Account:test' )
        else:
            messages.info(request, 'E-mail ou le mot de passe est incorrect')

        context = {
            "form" : form
        }
        return render(request, self.template_name, context)

class LogoutView(View):
    def get(self, request):
        logout(request)
        return myredirect( 'Account:login' )

@method_decorator(decorator_login, name='dispatch')
class HomeView(View):
    template_name = 'Registration/home.html'
    def get(self, request):
        context = {
            "home_active" : "active",
            "title_section" : "Home"
        }
        return render(request, self.template_name, context)

        
#endregion

#region Member Management

from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
#, DjangoUnicodeDecodeError

from django.contrib.sites.shortcuts import get_current_site
from Utils.functions import token_generator

#only admin can acces this page
import json 
@method_decorator(decorator_login, name='dispatch')
@method_decorator(decorator_user(['admin', 'encadrant']), name = 'dispatch')
class AddMember(View):
    template_name = 'Registration/addmember.html'
    template_memebers_list = 'Registration\jsPages\members.html'

    def getContext(self):
        context = {
            "addMember_active" : "active",
            "title_section" : "Add Member "
        }
        return context

    def getMemberData(self, members):
        #get data ready to use in html easily
        data = []
        for member in members:
            theObject = {}
            theObject['id'] = member.id
            theObject['email'] = member.email
            theObject['userType'] = MemberModel.TYPES[member.userType][1]
            theObject['signed'] = member.signed
            theObject['active'] = member.active
            theObject['date'] = member.date
            data.append(theObject)
        return data

    def searshFilter(self, members, search):
        filterMember = []
        for item in members:
            if search in item.email:
                filterMember.append(item)
        return filterMember

    def getOrderedListMember(self, datafor):
        dataform = json.loads(datafor)
        print(dataform)
        search = dataform['search']
        sortType = dataform['sortType']
        order = dataform['order']

        reverse = '-' if  order == 'Descendant' else ''
        #__contains is Django ORM's equivalent to SQL's LIKE keyword.
        #email__contains=f'%{searsh}%'
        filterMember = MemberModel.objects.all()
        if order == 'status':
            filterMember = filterMember.order_by(f'{reverse}signed', f'{reverse}active')
        else:
            filterMember = filterMember.order_by(f'{reverse}{sortType}')
        
        filterMember = self.searshFilter(filterMember, search)
        return self.getMemberData(filterMember)

    def getDefaultPage(self, request):
        form = AddMemberModelForm()
        context = self.getContext()
        context["form"] = form
        return render(request, self.template_name, context)
    
    def getMemberList(self, request):     
        context = {
            "members" : self.getOrderedListMember(request.GET.get('dataform'))
        }
        return render(request, self.template_memebers_list, context)       

    def get(self, request, theType = None):
        print(f'-->{theType}')
        if theType == None:
            return self.getDefaultPage(request)
        
        elif theType == 'memberList':
             #javascript member.js setMemberContent()
            return self.getMemberList(request)

    #POST ======================================
    #POST ======================================

    def addMember(self, request):
        form = AddMemberModelForm(request.POST)
     
        email = request.POST.get('email')
        if request.user.email == email:
            return HttpResponseBadRequest("impossible d'ajouter votre e-mail")
        if form.is_valid():
            form.save()
        else:
            return HttpResponseBadRequest("l'email existe déjà ")
        return HttpResponse()

    def deleteMember(self, request):
        print("---> delete")
        id = request.POST.get('id')

        member = MemberModel.objects.get(id= int(id))
        user = UserAccount.objects.filter(email = member.email)
        if user.exists():
            user[0].delete()
        else:
            member.delete()
        return HttpResponse()
        

    def post(self, request, theType = None):
        if theType == 'add':
            return self.addMember(request)
        elif theType == 'delete':
            return self.deleteMember(request)


class CheckEmailView(View):
    template_name = 'Registration/check_email.html'

    def get(self, request):
        form = CheckEmailForm()
        context = {
            "form" : form
        }
        return render(request, self.template_name, context)
    
    def sendEmail(self, request, member):
        #transform the email to encoded text for safe url
        uidb64 = urlsafe_base64_encode(force_bytes(member.email))
        domain = get_current_site(request).domain
        link = reverse('Account:memberRegister', kwargs={
            'uidb64' : uidb64,
            'token' : token_generator.make_token(member),
        })
        activate_url = 'http://' + domain + link

        send_mail(
            'Lien de vérification ',
            f'cliquez sur ce lien {activate_url} pour la vérification',
            'noreply@uit.ac.ma',
            [member.email],
            fail_silently=True,
        )
        print(activate_url)

    def post(self, request):
        form = CheckEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            member = MemberModel.objects.filter(email = email)[0]
            alreadySigned = member.signed
            if alreadySigned:
                return myredirect('Account:login')
            else:
                self.sendEmail(request, member)
        context = {
            "form" : form
        }
        return render(request, self.template_name, context)
    
class MemberRegister(View):
    encadrant_register_template = 'Registration/registerEncadrant.html'
    doctorant_register_template = 'Registration/registerDoctorant.html'

    def saveMember(self, member):
        #member.signed = True
        #member.save()
        pass

    def doctorantUpdate(self, request, member, user):
        form1 = UserForm(instance = user)
        doctorant = DoctorantModel.objects.filter(user = user)
        if doctorant.exists():
            form2 = DoctorantModelForm(instance=doctorant[0])
        else:
            form2 = DoctorantModelForm()
        if request.method == "POST":
            form1 = UserForm(request.POST, instance = user)
            if doctorant.exists():
                form2 = DoctorantModelForm(request.POST, instance=doctorant[0])
            else:
                form2 = DoctorantModelForm(request.POST)
            if form1.is_valid() and form2.is_valid():
                user = form1.updateUser(member)
                if doctorant.exists():
                    form2.save()
                else:
                    form2.saveDoctorant(user)
                self.saveMember(member)
                #return myredirect('Account:login')
        context = {"form1" : form1,"form2" : form2,}
        return render(request, self.doctorant_register_template, context)
    
    def encadrantUpdate(self, request, member, user):
        form1 = UserForm(instance = user)
        encadrant = EncadrantModel.objects.filter(user = user)
        if encadrant.exists():
            form2 = EncadrantModelForm(instance=encadrant[0])
        else:
            form2 = EncadrantModelForm()
        if request.method == "POST":
            form1 = UserForm(request.POST, instance = user)
            if encadrant.exists():
                form2 = EncadrantModelForm(request.POST, instance=encadrant[0])
            else:
                form2 = EncadrantModelForm(request.POST)
            if form1.is_valid() and form2.is_valid():
                user = form1.updateUser(member)
                if encadrant.exists():
                    form2.save()
                else:
                    form2.saveEncadrant(user)
                self.saveMember(member)
                #return myredirect('Account:login')
        context = {"form1" : form1,"form2" : form2,}
        return render(request, self.doctorant_register_template, context)

    def doctorant(self, request, member):
        data1 = {
            'first_name': 'ayoub', 
            'last_name': 'benhamou',
        }
        data2 = {
            'apogee' : '15263545',
            'cin' : 'GM452639'
        }
        form1 = UserForm(initial=data1)
        form2 = DoctorantModelForm(initial=data2)
        if request.method == "POST":
            form1 = UserForm(request.POST)
            form2 = DoctorantModelForm(request.POST)
            if form1.is_valid() and form2.is_valid():
                user = form1.saveUser(member)
                form2.saveDoctorant(user)
                self.saveMember(member)
                return myredirect('Account:login')

        context = {"form1" : form1,"form2" : form2,}
        return render(request, self.doctorant_register_template, context)
    
    def encadrant(self, request, member):
        data1 = {
            'first_name': 'ayoub', 
            'last_name': 'benhamou',
        }
        form1 = UserForm(initial=data1)
        form2 = EncadrantModelForm()
        if request.method == "POST":
            form1 = UserForm(request.POST)
            form2 = EncadrantModelForm(request.POST)
            if form1.is_valid() and form2.is_valid():
                user = form1.saveUser(member)
                form2.saveEncadrant(user)
                self.saveMember(member)
                #return myredirect('Account:login')
        
        context = {"form1" : form1,"form2" : form2,}
        return render(request, self.encadrant_register_template, context)
        
    def successToken(self, request, member):
        # if Account exist (member deleted and added again)
        # when member delete his account does not deleted
        # so we will just override informations
        userAccount = UserAccount.objects.filter(email = member.email)
        if userAccount.exists():
            if member.userType == MemberModel.ENCADRANT:
                return self.encadrantUpdate(request, member, userAccount[0])
            if member.userType == MemberModel.DOCTORANT:
                return self.doctorantUpdate(request, member, userAccount[0])
    
        #create new account for member
        if member.userType == MemberModel.ENCADRANT:
            return self.encadrant(request, member)
        if member.userType == MemberModel.DOCTORANT:
            return self.doctorant(request, member)
        return render(request, P_error)

    def checkTocken(self, request, uidb64, token):
        try:
            email = force_text(urlsafe_base64_decode(uidb64) ) 
            member = MemberModel.objects.get(email = email)
            is_valid_token = token_generator.check_token(member, token)
            if is_valid_token:
                is_already_signed = member.signed
                if is_already_signed:
                    return myredirect('Account:login')
                return self.successToken(request, member)
        except Exception as e:
            print("MemberRegister Link Error")
            pass
        return  render(request, P_error)

    def get(self, request, uidb64, token):
        return self.checkTocken(request, uidb64, token)
    
    def post(self, request, uidb64, token):
        return self.checkTocken(request, uidb64, token)

#endregion
