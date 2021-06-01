#region import
from django.shortcuts import render,HttpResponse
from django.urls import reverse
from django.views import View
from django.contrib.auth.models import Group
from django.http import HttpResponseBadRequest
import json 


from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

#Custom
from .authenticate import unauthenticated_user, allowed_users, dedicated
from Utils.functions import myredirect, current_milli_time
from Utils.const import *


from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

#member management
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text


from django.contrib.sites.shortcuts import get_current_site
from Utils.functions import token_generator, deleteUser


from .forms import (
    AddMemberModelForm,
    UserLogin,
    CheckEmailForm,

    DoctorantModelForm,
    UserForm,
    EncadrantModelForm,

    DoctorantUpdateModelForm,
    UserUpdateForm,
    EncadrantUpdateModelForm,
    UpdatePasswordModelFrom,
)

from .models import (
    MemberModel,
    DoctorantModel,
    EncadrantModel,
    UserAccount,
    DoctorantRelation,
)

# region decorator

decorator_login = [login_required(login_url='/login/')]
decorator_auth = [unauthenticated_user]
decorator_dedicated = [dedicated]
def decorator_user(allowed_roles):
    return [allowed_users(allowed_roles=allowed_roles)]

# endregion

# endregion

# region Register


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
                return myredirect( 'Account:home' )
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
    def get(self, request):
        return myredirect('Compt:posts')

        
#endregion

# region Member Management

@method_decorator(decorator_login, name='dispatch')
@method_decorator(decorator_user(['admin']), name = 'dispatch')
class MemberManagement(View):
    template_name = 'Registration/addmember.html'
    template_memebers_list = 'Registration\jsPages\members.html'
    template_relations = 'Registration\include\list_relations.html'

    def getContext(self):
        context = {
            "addMember_active" : "active",
            "title_section" : "Add Member "
        }
        return context


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
        print(f'------{sortType}')
        if sortType == 'status ':
            filterMember = filterMember.order_by(f'{reverse}signed', f'{reverse}active')
        else:
            filterMember = filterMember.order_by(f'{reverse}{sortType}')
        
        return self.searshFilter(filterMember, search)
        #return self.getMemberData(filterMember)

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
    
    def getAccount(self, request):
        id = request.GET.get('id')
        member = MemberModel.objects.get(id= int(id))
        user = UserAccount.objects.get(email = member.email)
        lien = ""
        if member.userType == MemberModel.ENCADRANT:
            lien = reverse('Account:updateAccount', kwargs={'userType':'encadrant', 'accountId' : user.id})
        else:
            lien = reverse('Account:updateAccount', kwargs={'userType':'doctorant', 'accountId' : user.id})
        return HttpResponse(lien)

    def getRelations(self, request):
        id = request.GET.get('id')
        try:
            member = MemberModel.objects.get(id= int(id))
            user = UserAccount.objects.get(email = member.email)
            f_relations = []
            if member.userType == MemberModel.ENCADRANT:
                relations = DoctorantRelation.objects.filter(encadrant = user)
                for item in relations:
                    r = {}
                    r["id"] = item.id
                    r["email"] = item.doctorant.email
                    r["getRelationType"] = item.getRelationName()
                    f_relations.append(r)
            elif member.userType == MemberModel.DOCTORANT:
                relations = DoctorantRelation.objects.filter(doctorant = user)
                for item in relations:
                    r = {}
                    r["id"] = item.id
                    r["email"] = item.encadrant.email
                    r["getRelationType"] = item.getRelationName()
                    f_relations.append(r)
            
            context = {
                "relations" : f_relations
            }
            return render(request, self.template_relations, context)
        except Exception as e:
            return HttpResponseBadRequest()

    def get(self, request, theType = None):
        print(f'-->{theType}')
        if theType == None:
            return self.getDefaultPage(request)
        
        elif theType == 'memberList':
            return self.getMemberList(request)
        
        elif theType == 'account':
            return self.getAccount(request)
        
        elif theType == 'relations':
            return self.getRelations(request)

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
        print(f"---> {id}")

        member = MemberModel.objects.get(id= int(id))
        user = UserAccount.objects.filter(email = member.email)
        if user.exists():
            deleteUser(user)
        member.delete()
        return HttpResponse()
    
    def deactivateMember(self, request):
        print("--------------------deactivateMember")
        id = request.POST.get('id')

        try:
            member = MemberModel.objects.get(id= int(id))
            print(member)
            member.active = not member.active
            member.save()
        except Exception as e:
            return HttpResponseBadRequest()
        return HttpResponse() 

    def associerMember(self, request):
        try:
            print("--------------------Accocier")
            id = request.POST.get('id')
            email = str(request.POST.get('memberEmail')).strip()
            relationType = int(request.POST.get('relationType'))

            print(f'-->{id}-')
            print(f'-->{relationType}-')
            print(f'-->{email}-')

            targetMember = MemberModel.objects.get(id = id)
            targetUser = UserAccount.objects.get(email = targetMember.email) 
            userAsscociated = UserAccount.objects.get(email = email)

            relation = None
            if targetMember.isEncadrant():
                relation = DoctorantRelation(
                    doctorant = userAsscociated, 
                    encadrant = targetUser, 
                    relationType = relationType)
            
            if targetMember.isDoctorant():
                relation = DoctorantRelation(
                    doctorant = targetUser, 
                    encadrant = userAsscociated, 
                    relationType = relationType)
            
            
            if not relation.isValide()[0]:
                return HttpResponseBadRequest(relation.isValide()[1])
            
            relation.save()
            return HttpResponse('La relation a été créée avec succès')
        except Exception as e:
            return HttpResponseBadRequest()

    def deleteRelation(self, request):
        print("--------------------Delete relation")
        id = request.POST.get('id')
        relation = DoctorantRelation.objects.get(id = int(id))
        relation.delete()
        return HttpResponse('suppression réussie de la relation ')

    def post(self, request, theType = None):
        if theType == 'add':
            return self.addMember(request)
        elif theType == 'delete':
            return self.deleteMember(request)
        elif theType == 'deactivate':
            return self.deactivateMember(request)
        elif theType == 'associate':
            return self.associerMember(request)
        elif theType == 'deleteRelation':
            return self.deleteRelation(request)

@method_decorator(decorator_auth, name = 'dispatch')
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

@method_decorator(decorator_auth, name = 'dispatch')   
class MemberRegister(View):
    encadrant_register_template = 'Registration/registerEncadrant.html'
    doctorant_register_template = 'Registration/registerDoctorant.html'

    def saveMember(self, member):
        member.signed = True
        member.save()

    def doctorant(self, request, member):
        form1 = UserForm()
        form2 = DoctorantModelForm()
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
        form1 = UserForm()
        form2 = EncadrantModelForm()
        if request.method == "POST":
            form1 = UserForm(request.POST)
            form2 = EncadrantModelForm(request.POST)
            if form1.is_valid() and form2.is_valid():
                user = form1.saveUser(member)
                form2.saveEncadrant(user)
                self.saveMember(member)
                return myredirect('Account:login')
        
        context = {"form1" : form1,"form2" : form2,}
        return render(request, self.encadrant_register_template, context)
        
    def successToken(self, request, member):
        # if already has an account
        userAccount = UserAccount.objects.filter(email = member.email)
        if userAccount.exists():
            return myredirect('Account:login')
    
        # else create new account for member
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
                return self.successToken(request, member)
        except Exception as e:
            print("MemberRegister Link Error")
            pass
        return render(request, P_error)

    def get(self, request, uidb64, token):
        return self.checkTocken(request, uidb64, token)
    
    def post(self, request, uidb64, token):
        return self.checkTocken(request, uidb64, token)

#endregion

# region Account Update

@method_decorator(decorator_login, name='dispatch')
class AccountUpdate(View):
    temp_encadrant = 'Registration/account/encadrant.html'
    temp_doctorant = 'Registration/account/doctorant.html'

    def getContext(self):
        context = {
            "title_section" : "Account"
        }
        return context

    def getDoctorantForm(self, doctorant, request, post):
        allowed = request.user.isAdmin() or DoctorantRelation.objects.filter(encadrant = request.user, relationType = 0).exists()
        if not post:
            if allowed:
                return DoctorantUpdateModelForm(False, instance = doctorant)
            else:
                return DoctorantUpdateModelForm(True, instance = doctorant)
        else:
            if allowed:
                return DoctorantUpdateModelForm(False, request.POST, instance = doctorant)
            else:
                return DoctorantUpdateModelForm(True, request.POST, instance = doctorant)    

    def doctorant(self, request, user):
        context = self.getContext()
        
        doctorant = DoctorantModel.objects.get(user = user)

        form1 = UserUpdateForm(instance = user)
        form2 = self.getDoctorantForm(doctorant, request, False)
        
        if request.method == "POST":
            form1 = UserUpdateForm(request.POST, request.FILES, instance = user)
            form2 = self.getDoctorantForm(doctorant, request, True)
            if form1.is_valid() and form2.is_valid():
                form1.save()
                form2.save()
        
        context["form1"] = form1
        context["form2"] = form2
        context['userId'] = user.id
        return render(request, self.temp_doctorant, context)

    def encadrant(self, request, user):
        context = self.getContext()
        
        encadrant = EncadrantModel.objects.get(user = user)

        form1 = UserUpdateForm(instance = user)
        form2 = EncadrantUpdateModelForm(instance = encadrant)
        
        if request.method == "POST":
            form1 = UserUpdateForm(request.POST, request.FILES, instance = user)
            form2 = EncadrantUpdateModelForm(request.POST, instance = encadrant)
            if form1.is_valid() and form2.is_valid():
                form1.save()
                form2.save()
        
        context["form1"] = form1
        context["form2"] = form2
        context['userId'] = user.id
        return render(request, self.temp_encadrant, context)

    def getAccount(self, request, userType, id, fromMember):
        user = None
        if fromMember:
            member = MemberModel.objects.get(id = id)  
            user = member.user
        else:
            user = UserAccount.objects.get(id = id)
        if userType == 0:
            return self.encadrant(request, user)
        else:
            return self.doctorant(request, user)


    def getPage(self, request, userType, accountId):
        if userType == 'encadrant_member':
            return self.getAccount(request, 0, accountId, True)
        if userType == 'doctorant_member':
            return self.getAccount(request, 1, accountId, True)
        if userType == 'encadrant_account':
            return self.getAccount(request, 0, accountId, False)
        if userType == 'doctorant_account':
            return self.getAccount(request, 1, accountId, False)
        return render(request, P_404)
        

    def get(self, request, userType, accountId):
        return self.getPage(request, userType, accountId)
    
    def post(self, request, userType, accountId):
        return self.getPage(request, userType, accountId)

class ChangePassword(View):
    tmp_changePasword = 'Registration/account/change_password.html'

    def page(self, request, userId):
        form = UpdatePasswordModelFrom()
        if request.POST:
            user = UserAccount.objects.get(id = userId)
            form = UpdatePasswordModelFrom(request.POST, instance=user)
            
            if form.is_valid:
                messages.info(request, 'Le mot de passe a été changé avec succès ')
                password = form['password'].value()
                user.set_password(password)
                user.save()
                login(request, user)

        context = {
            'form' : form
        }
        return render(request, self.tmp_changePasword, context)

    def get(self, request, userId):
        return self.page(request, userId)
    
    def post(self, request, userId):
        return self.page(request, userId)

# endregion