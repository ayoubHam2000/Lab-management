from django.shortcuts import render, HttpResponse
from django.http import HttpResponseBadRequest
from django.urls import reverse
from django.views import View

#Utilities
import json

#Custom
from Account.authenticate import unauthenticated_user, allowed_users
from Utils.functions import myredirect, current_milli_time
from Utils.const import *

#decorators
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
decorator_login = [login_required(login_url='/login/')]
decorator_auth = [unauthenticated_user]
def decorator_user(allowed_roles):
    return [allowed_users(allowed_roles=allowed_roles)]

#forms and models
from .forms import PostModelForm

from .models import PostModel, PostCommentModel
from Account.models import DoctorantRelation, UserAccount

@method_decorator(decorator_login, name='dispatch')
class PostsView(View):
    temp_post = 'Posts/post.html'
    temp_all_post = 'Posts/js_posts.html'

    def getContext(self):
        context = {
            "title_section" : "Home"
        }
        return context


    def getEquipe(self, request):
        user = request.user
        if user.isEncadrant():
            mesDoctorants = DoctorantRelation.objects.filter(encadrant = user, relationType = 0)
            c_mesDoctorant = DoctorantRelation.objects.filter(encadrant = user, relationType = 1)

            doctorants = [x.doctorant for x in mesDoctorants]
            co_encadrant_equipe = DoctorantRelation.objects.filter(doctorant__in = doctorants, relationType = 1)
            return mesDoctorants, c_mesDoctorant, co_encadrant_equipe, 'encadrant'
        
        if user.isDoctorant():
            monEncadrant = DoctorantRelation.objects.filter(doctorant = user, relationType = 0)
            mes_co_encadrants = DoctorantRelation.objects.filter(doctorant = user, relationType = 1)
            doctorants = [] if not monEncadrant.exists() else DoctorantRelation.objects.filter(encadrant = monEncadrant[0].encadrant, relationType = 0)
            return monEncadrant, mes_co_encadrants, doctorants, 'doctorant'
        
        return [], [], [], 0
        

    def getPage(self, request):
        form = PostModelForm()

        context = self.getContext()
        context['form'] = form
        data = self.getEquipe(request)
        context['list1'] = data[0]
        context['list2'] = data[1]
        context['list3'] = data[2]
        context['relationType'] = data[3]
        return render(request, self.temp_post, context)

    def getPosts(self, request):
        posts = PostModel.objects.filter().order_by('-date')
        context = {
            'posts' : posts
        }
        return render(request, self.temp_all_post, context)


    def get(self, request, theType = None):
        if theType == None:
            return self.getPage(request)
        elif theType == 'posts':
            return self.getPosts(request)

    def post(self, request, theType = None):
        form = PostModelForm(user = request.user, data = request.POST, files = request.FILES)
        if form.is_valid:
            #print('Is Valide')
            form.save()
        return self.get(request)

class CommentView(View):
    def post(self, request, id):
        try:
            thePost = PostModel.objects.get(id = id)
            user = request.user.email
            text = request.POST.get('text')
            comment = PostCommentModel(user = user, post = thePost, text = text)
            comment.save()

            # json response
            user = comment.getUser()
            response_data = {}
            response_data['getImage'] = user.getImage()
            response_data['getFullName'] = user.getFullName()
            response_data['date'] = comment.getDate()
            response_data['comment'] = text

            return HttpResponse(json.dumps(response_data), content_type="application/json")
        except Exception as e:
            return HttpResponseBadRequest(e)

