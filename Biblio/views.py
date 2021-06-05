#region import 
from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from Utils.const import *

from .models import PublicationModel, AuteurModel

from .forms import PublicationModelForm, AddAuteurForm

from Utils.functions import myredirect

import json  

from Account.authenticate import allowed_users
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
decorator_login = [login_required(login_url='/login/')]


#endregion


#region Bib
@login_required(login_url='/login/')
def Ajouter(request):
	def getAuteurList():
		l = AuteurModel.objects.all()
		return l

	form = PublicationModelForm() 
	if request.POST :
		form = PublicationModelForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return myredirect('Biblio:information')
			
	context ={
		"biblio_active" : "active",
		"form" : form,
		"title_section" : "Bibliotheque",
		"auteurs" : getAuteurList()
	 }
		 
	return render(request,'Biblio/ajouter.html', context)

#la fonction sert a modifier un block d'informations (une formulaire precise)
#le parametre id sert a definir une formulaire precise chaque formulaire a un identificateurs precise definie par django
@login_required(login_url='/login/')
def update(request, f_id):
	#get
	formulaire = PublicationModel.objects.get(id = f_id)
	form = PublicationModelForm(instance = formulaire)

	if request.POST:
		form = PublicationModelForm(request.POST, request.FILES, instance = formulaire)
		if form.is_valid():         
			form.save()
			return myredirect('Biblio:information')
	
	context ={

		"biblio_active" : "active",
		"form" : form,
		"title_section" : "Bibliotheque",
		"auteurs" : AuteurModel.objects.all()
		
	 }
		 
	return render(request,'Biblio/ajouter.html', context)


def searchAuteur(auteur):
	listAuteurs = []
	formulaires = PublicationModel.objects.all()
	for item in formulaires:
		if item.pr_auteur == auteur or auteur in item.co_auteur.split(","):
			listAuteurs.append(item)
	return listAuteurs
			
#cette fonction sert a la recherche (a partir de la barre de recherche )
@login_required(login_url='/login/')
def pagebib(request):
	searchType = request.GET.get("searchType")
	search = request.GET.get("mySearch")

	if search == None or search == "":            
		formulaires = PublicationModel.objects.filter()
	else:
		if searchType == 'auteur':
			formulaires = searchAuteur(search)
		if searchType == 'titre':
			formulaires = PublicationModel.objects.filter(titre = search)
		if searchType == 'journal':
			formulaires = PublicationModel.objects.filter(journal = search)
		if searchType == 'doi':
			formulaires = PublicationModel.objects.filter(doi = search)
		if searchType == 'issn':
			formulaires = PublicationModel.objects.filter(issn = search)

	arr = []
	length = len(formulaires)
	for i in range(0, length):
		arr.append(formulaires[length - 1 - i])
	print(arr)

	#formulaires = formulaires.order_by('-date')
	context ={
		"biblio_active" : "active",
		"formulaires" : arr,
		"title_section" : "Bibliotheque"
	}

	if len(PublicationModel.objects.all()) == 0:   # cette partie si on n'a aucune formulaire 
		return render(request,'Biblio/empty_bib.html',context)


	return render(request,'Biblio/page_biblio.html', context)


@allowed_users(allowed_roles=['admin', 'superadmin', 'encadrant'])
def deleteF(request, id_F):
	if request.POST:
		formulaire = PublicationModel.objects.filter(id = id_F)
		formulaire.delete()
		return myredirect('Biblio:information')

@method_decorator(decorator_login, name='dispatch')
class searchbib(View):   #c'est la nouvelle version de la partie de recherche 
	template = 'Biblio/searchbar.html'

	def getAsJson(self, type, data):
		response_data = {}
		response_data[type] = data
			
		return HttpResponse(
			json.dumps(response_data),
			content_type='application/json'
		)
	
	def getList(self, type):
		theList = PublicationModel.objects.order_by().values(type).distinct()
		data = []
		for item in theList:
			data = data + [item.get(type)]
		return self.getAsJson(type, data)

	def getListAuteur(self):
		s_type = ['pr_auteur', 'co_auteur'] 

		pr_auteurs = PublicationModel.objects.order_by().values(s_type[0]).distinct()
		co_auteurs = PublicationModel.objects.order_by().values(s_type[1]).distinct()

		data1 = []
		for item in pr_auteurs:
			theList = [item.get(s_type[0])]
			data1 = data1 + theList
		
		data2 = []
		for item in co_auteurs:
			#it has to be at least one co_auteur
			theList = item.get(s_type[1]).split(",")
			data2 = data2 + theList

		data = {
			'pr_auteurs' : data1,
			'co_auteurs' : data2,
		}
		return self.getAsJson('auteur', data)

	def pageRecherche(self, request):
		context = {
		}
		return render(request, self.template, context)

	def get(self, request, type = None):
		#print(type)
		if type == None:
			return self.pageRecherche(request)
		else:
			if type == 'auteur':
				return self.getListAuteur()
			return self.getList(type)
			
#endregion

class AuteurViw(View):
	tmp_auteur = 'Auteur/auteur.html'

	def getContext(self):
		context = {}
		return context

	def getAuteurList(self):
		l = AuteurModel.objects.all()
		return l

	def defaultPage(self, request):
		form = AddAuteurForm()
		context = self.getContext()

		if request.POST:
			form = AddAuteurForm(request.POST)
			if form.is_valid():
				form.save()

		context['form'] = form
		context['auteurs'] = self.getAuteurList()
		return render(request, self.tmp_auteur, context)


	def get(self, request, action = None):
		return self.defaultPage(request)

	def delete(self, request):
		id = request.POST.get('id')
		obj = AuteurModel.objects.get(id = id)
		obj.delete()
		return myredirect('Biblio:auteurs')

	def post(self, request, action = None):
		if action == None:
			return self.defaultPage(request)
		elif action == 'delete':
			return self.delete(request)
		return render(request, P_404)

