#region import 
from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from Utils.const import *

from .models import PublicationModel, UserAccount

from .forms import PublicationModelForm

from Utils.functions import myredirect

import json  

from Account.authenticate import allowed_users
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
decorator_login = [login_required(login_url='/login/')]


#endregion


#region Bib
@method_decorator(decorator_login, name='dispatch')
class AddPublication(View):
	tmp_add_publication = 'Biblio/ajouter.html'

	def getContext(self):
		return {
			"biblio_active" : "active",
			"title_section" : "Bibliotheque",
		}

	def getTestData(self):
		return {
			'titre' : 'titre',
			'type_pub' : 'journal',
			'doi' : '120',
			'volume' : '20',
			'pr_page' : '20',
			'der_page' : '20',
			'citation' : '20',
			'journal' : 'le journal de matin',
			'issn' : '125480',
			'publisher' : 'the publisher'
		}


	def defaultPage(self, request):
		form = PublicationModelForm() 
		#form = PublicationModelForm(self.getTestData())

		if request.POST:
			form = PublicationModelForm(request.POST, request.FILES)
			if form.is_valid():
				pub = form.save(commit=False)
				pub.user_publisher = request.user
				pub.save()
				return myredirect('Biblio:information')

		context = self.getContext()
		context['form'] = form
		return render(request, self.tmp_add_publication, context)

	def get(self, request):
		return self.defaultPage(request)
	
	def post(self, request):
		return self.defaultPage(request)

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
		"title_section" : "Bibliotheque"
		
	 }
		 
	return render(request,'Biblio/ajouter.html', context)


def searchAuteur(auteur):
	formulaires = PublicationModel.objects.filter()
	res = []
	for item in formulaires:
		if auteur in item.pr_auteur or auteur in item.co_auteur:
			res.append(item)
	return res
			
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

	# reverse formulaires
	arr = []
	length = len(formulaires)
	for i in range(0, length):
		arr.append(formulaires[length - 1 - i])

	context ={
		"biblio_active" : "active",
		"formulaires" : arr,
		"title_section" : "Bibliotheque"
	}

	if len(PublicationModel.objects.all()) == 0:   # cette partie si on n'a aucune formulaire 
		return render(request,'Biblio/empty_bib.html',context)


	return render(request,'Biblio/page_biblio.html', context)


@login_required(login_url='/login/')
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
		#s_type = ['pr_auteur', 'co_auteur'] 
		data = PublicationModel.getAllAuthors()
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


