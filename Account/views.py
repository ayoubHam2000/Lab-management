#region import
from django.shortcuts import render,HttpResponse, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth.models import Group
from django.http import HttpResponseBadRequest
from django.db.models import Q
import json 


from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

#Custom
from .authenticate import unauthenticated_user, allowed_users
from Utils.functions import myredirect, current_milli_time
from Utils.const import *
import re 


from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

#user management
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text


from django.contrib.sites.shortcuts import get_current_site
from Utils.functions import token_generator, deleteUser, get_object_or_404


from .forms import (
    UserLogin,
    AddUserForm,
    CheckEmailForm,

    UserForm,
    DoctorantModelForm,
    EncadrantModelForm,

    UserUpdateForm,
    DoctorantUpdateModelForm,
    EncadrantUpdateModelForm,
    UpdatePasswordModelFrom,
)

from .models import (
    UserAccount,
    DoctorantModel,
    EncadrantModel,
    RelationModel,
)

# region decorator

decorator_login = [login_required(login_url='/login/')]
decorator_auth = [unauthenticated_user]
def decorator_user(allowed_roles):
    return [allowed_users(allowed_roles=allowed_roles)]

# endregion

# endregion

# region Register


# if already login go to home page
@method_decorator(decorator_auth, name = 'dispatch')
class LoginView(View):
    template_name = 'Registration/login.html'

    def get(self, request):
        form = UserLogin()
        context = {
            "form" : form
        }
        return render(request, self.template_name, context)

      
    def post(self, request):
        form = UserLogin()
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        user = authenticate(request, email = email, password = password)

        if user is not None:
            if not user.is_active:
                messages.info(request, 'votre compte est désactivé')
            elif not user.is_signed:
                return myredirect('Account:checkEmail')
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

class HomeView(View):
    def get(self, request):
        return myredirect('Compt:posts')

        
#endregion

# region Users Management

@method_decorator(decorator_login, name='dispatch')
@method_decorator(decorator_user(['admin', 'superadmin']), name = 'dispatch')
class UsersManagement(View):
    template_name = 'Registration/addmember.html'
    template_memebers_list = 'Registration/jsPages/members.html'
    template_relations = 'Registration/include/list_relations.html'

    def getContext(self):
        context = {
            "addMember_active" : "active",
            "title_section" : "Ajouter des utilisateurs"
        }
        return context

    def searshFilter(self, users, search):
        filterMember = []
        for item in users:
            if search in item.email:
                filterMember.append(item)
        return filterMember

    def sortWithUserType(self, users):
        return users

    def sortWithStatus(self, users):
        return users

    def getOrderedListUsers(self, data):
        # sortType : date_joined, email, userType, status -> addmember.html/orderModal
        dataform = json.loads(data)
        search = dataform['search']
        sortType = dataform['sortType']
        order = dataform['order']

        reverse = '-' if  order == 'Descendant' else ''
        filterMember = UserAccount.objects.all()
        if sortType == 'status':
            filterMember = self.sortWithStatus(filterMember)
        elif sortType == 'userType':
            filterMember = self.sortWithUserType(filterMember)
        else:
            filterMember = filterMember.order_by(f'{reverse}{sortType}')
        
        return self.searshFilter(filterMember, search)

    def getDefaultPage(self, request):
        form = AddUserForm(request.user)

        context = self.getContext()
        context["form"] = form
        return render(request, self.template_name, context)
    
    def getUsersList(self, request):
        context = {
            "users" : self.getOrderedListUsers(request.GET.get('dataform'))
        }
        return render(request, self.template_memebers_list, context)
    
    def getRelations(self, request):
        id = request.GET.get('id')
        try:
            user = UserAccount.objects.get(id= int(id))
            relations = RelationModel.objects.filter(user1 = user)    
            context = {
                "relations" : relations
            }
            return render(request, self.template_relations, context)
        except Exception as e:
            return HttpResponseBadRequest()

    def get(self, request, theType = None):
        if theType == None:
            return self.getDefaultPage(request)
        
        elif theType == 'usersList':
            #js member.js
            return self.getUsersList(request)
        
        elif theType == 'relations':
            #js member.js
            return self.getRelations(request)
        return render(request, P_404)

    #POST ======================================
    #POST ======================================

    def addUser(self, request):
        form = AddUserForm(request.user, request.POST)
     
        email = request.POST.get('email').lower()
        if request.user.email == email:
            return HttpResponseBadRequest("l'email existe déjà")
        if form.is_valid():
            form.save()
        else:
            return HttpResponseBadRequest("l'email existe déjà ")
        return HttpResponse()

    def deleteUser(self, request):
        id = request.POST.get('id')

        try:
            user = UserAccount.objects.get(id= int(id))
            user.delete()
            return HttpResponse()
        except:
            return HttpResponseBadRequest()
    
    def deactivateUser(self, request):
        id = request.POST.get('id')

        try:
            user = UserAccount.objects.get(id= int(id))
            user.is_active = not user.is_active
            user.save()
        except Exception as e:
            return HttpResponseBadRequest()
        return HttpResponse() 

    def associerRelation(self, request):
        try:
            id = request.POST.get('id')
            email = str(request.POST.get('memberEmail')).strip().lower()
            relationType = int(request.POST.get('relationType'))

            user1 = UserAccount.objects.get(id = id)
            user2 = UserAccount.objects.get(email = email)

            relation1 = RelationModel(user1 = user1, user2 = user2, relationType = relationType)
            relation2 = RelationModel(user1 = user2, user2 = user1, relationType = relationType)

            if not relation1.isValide()[0]:
                return HttpResponseBadRequest(relation1.isValide()[1])
            
            relation1.save()
            relation2.save()
            return HttpResponse('la création de la relation est bien effectué')
        except Exception as e:
            return HttpResponseBadRequest()

    def deleteRelation(self, request):
        try:
            id = request.POST.get('id')
            relation1 = RelationModel.objects.get(id=int(id))
            relation2 = RelationModel.objects.get(user1=relation1.user2, 
            user2=relation1.user1, 
            relationType=relation1.relationType)
            relation1.delete()
            relation2.delete()
            return HttpResponse('la suppression est effectué')
        except:
            return HttpResponseBadRequest()

    def encadrant_switch_admin(self, request):
        try:
            id = request.POST.get('id')
            user = UserAccount.objects.get(id = int(id))
            user.userSwitchAdmin()
            return HttpResponse()
        except:
            return HttpResponseBadRequest()

    def post(self, request, theType = None):
        if theType == 'add':
            return self.addUser(request)
        elif theType == 'delete':
            return self.deleteUser(request)
        elif theType == 'deactivate':
            return self.deactivateUser(request)
        elif theType == 'associate':
            return self.associerRelation(request)
        elif theType == 'deleteRelation':
            return self.deleteRelation(request)
        elif theType == 'encadrant_switch_admin':
            return self.encadrant_switch_admin(request)
        return render(request, P_404)

@method_decorator(decorator_auth, name = 'dispatch')
class CheckEmailView(View):
    template_name = 'Registration/check_email.html'

    def get(self, request):
        form = CheckEmailForm()
        context = {
            "form" : form
        }
        return render(request, self.template_name, context)

    #POST ======================================
    #POST ======================================

    def sendEmail(self, request, user):
        #transform the email to encoded text for safe url
        uidb64 = urlsafe_base64_encode(force_bytes(user.email))
        domain = get_current_site(request).domain
        link = reverse('Account:userRegister', kwargs={
            'uidb64' : uidb64,
            'token' : token_generator.make_token(user),
        })
        activate_url = 'http://' + domain + link

        send_mail(
            'Lien de vérification ',
            f'cliquez sur ce lien {activate_url} pour la vérification',
            'noreply@uit.ac.ma',
            [user.email],
            fail_silently=True,
        )
        #print(activate_url)
        #return redirect(activate_url)

    def post(self, request):
        try:
            form = CheckEmailForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email').lower()
                user = UserAccount.objects.get(email = email)
                alreadySigned = user.hasAccount()
                if alreadySigned:
                    user.is_signed = True
                    user.save()
                    return myredirect('Account:login')
                else:
                    self.sendEmail(request, user)
            context = {
                "form" : form
            }
            return render(request, self.template_name, context)
        except:
            return render(request, P_404)

@method_decorator(decorator_auth, name = 'dispatch')   
class UserRegister(View):
    encadrant_register_template = 'Registration/registerEncadrant.html'
    doctorant_register_template = 'Registration/registerDoctorant.html'

    def saveUser(self, form):
        user = form.save(commit=False)
        user.is_signed = True
        user.save()
        return user

    def doctorant(self, request, user):
        form1 = UserForm(instance = user)
        form2 = DoctorantModelForm()
        if request.method == "POST":
            form1 = UserForm(request.POST, instance = user)
            form2 = DoctorantModelForm(request.POST)
            if form1.is_valid() and form2.is_valid():
                user = self.saveUser(form1)
                form2.saveDoctorant(user)
                return myredirect('Account:login')

        context = {"form1" : form1,"form2" : form2,}
        return render(request, self.doctorant_register_template, context)
    
    def encadrant(self, request, user):
        form1 = UserForm(instance = user)
        form2 = EncadrantModelForm()
        if request.method == "POST":
            form1 = UserForm(request.POST, instance = user)
            form2 = EncadrantModelForm(request.POST)
            if form1.is_valid() and form2.is_valid():
                user = self.saveUser(form1)
                form2.saveEncadrant(user)
                return myredirect('Account:login')
        
        context = {"form1" : form1,"form2" : form2,}
        return render(request, self.encadrant_register_template, context)
        
    def successToken(self, request, user):
        # if already has an account
        if user.is_signed:
            return myredirect('Account:login')
    
        # else create new account for member
        if user.isEncadrant():
            return self.encadrant(request, user)
        if user.isDoctorant():
            return self.doctorant(request, user)
        return render(request, P_404)

    def checkTocken(self, request, uidb64, token):
        try:
            email = force_text(urlsafe_base64_decode(uidb64) ) 
            user = UserAccount.objects.get(email = email)
            is_valid_token = token_generator.check_token(user, token)
            if is_valid_token:
                return self.successToken(request, user)
        except Exception as e:
            #print("UserRegister Link Error")
            pass
        return render(request, P_404)

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
            "title_section" : "Compte"
        }
        return context

    def doctorant(self, request, user):
        context = self.getContext()
        
        doctorant = DoctorantModel.objects.get(user = user)

        form1 = UserUpdateForm(instance = user)
        form2 = DoctorantUpdateModelForm(request.user, user, instance = doctorant)
        
        if request.method == "POST":
            form1 = UserUpdateForm(request.POST, request.FILES, instance = user)
            form2 = DoctorantUpdateModelForm(request.user, user, request.POST, instance = doctorant)
            if form1.is_valid() and form2.is_valid():
                form1.save()
                form2.save()
        
        context["form1"] = form1
        context["form2"] = form2
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
        return render(request, self.temp_encadrant, context)

    def getPage(self, request, accountId):
        try:
            user = UserAccount.objects.get(id = accountId)
            if user.isEncadrant():
                return self.encadrant(request, user)
            elif user.isDoctorant():
                return self.doctorant(request, user)
        except:
            pass
        return render(request, P_404)
        
    def get(self, request, accountId):
        return self.getPage(request, accountId)
    
    def post(self, request, accountId):
        return self.getPage(request, accountId)

class ChangePassword(View):
    tmp_changePasword = 'Registration/account/change_password.html'

    def isPasswordValide(self, password):
        #password regex
        r  = r"^(?=.*?[a-z])(?=.*?[0-9]).{8,}$"
        return re.match(r, password)

    def changePassword(self, request, user):
        form = UpdatePasswordModelFrom(request.POST, instance=user)
        
        if form.is_valid:
            password = form['password'].value()
            if self.isPasswordValide(password):
                messages.info(request, 'Le mot de passe a été changé avec succès ')
                user.set_password(password)
                user.save()
                login(request, user)
            else:
                form.add_error('password', STRONG_PASSWORD)
        return form

    def checkAccess(self, request, user):
        isTheSameUser = request.user.id == user.id
        if isTheSameUser:
            return isTheSameUser
        isAdmin = (request.user.isAdmin() and not user.isAdmin()) or request.user.isSuperAdmin()
        if isAdmin:
            return isAdmin
        return False

    def page(self, request, userId):
        form = UpdatePasswordModelFrom()
        try:
            user = UserAccount.objects.get(id = userId)
            #if other users try to change the password with link
            if not self.checkAccess(request, user):
                return render(request, P_404)
            if request.POST:
                form = self.changePassword(request, user)
            context = {
                'form' : form
            }
            return render(request, self.tmp_changePasword, context)
        except:
            return render(request, P_404)

    def get(self, request, userId):
        return self.page(request, userId)
    
    def post(self, request, userId):
        return self.page(request, userId)

# endregion