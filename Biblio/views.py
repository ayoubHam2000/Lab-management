#region import 
from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from Utils.const import *

from .models import PublicationModel, AuteurModel, UserAccount, AuteurRelationsModel

from .forms import PublicationModelForm, AddAuteurForm

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


	def saveAuteurs(self, pr_auteur, co_auteurs, pub):
		errors = []
		try:
			json_auteurs = json.loads(co_auteurs)
			ids = [int(x['id']) for x in json_auteurs]
			prauteur = AuteurModel.objects.filter(id = pr_auteur)
			coauteurs = AuteurModel.objects.filter(id__in=ids)
			if not prauteur.exists():
				errors.append('le champ premier auteur est vide')
			if not coauteurs.exists():
				errors.append('le champ co.auteur est vide')
			if pr_auteur in co_auteurs:
				errors.append('Les champs pr.auteur et co.auteur sont identiques')
			if len(errors) != 0:
				return errors

			pub.save()
			AuteurRelationsModel(auteur = prauteur[0], pub = pub, auteur_type=0).save()
			for item in coauteurs:
				AuteurRelationsModel(auteur = item, pub = pub, auteur_type=1).save()
			return errors
		except:
			errors.append("error")
			return errors
		

	def defaultPage(self, request):
		form = PublicationModelForm() 
		# form = PublicationModelForm(self.getTestData()) 
		auteursList =  AuteurModel.objects.all()

		if request.POST:
			form = PublicationModelForm(request.POST, request.FILES)
			pr_auteur = request.POST.get('pr_auteur')
			co_auteurs = request.POST.get('co_auteurs')
			if form.is_valid():
				pub = form.save(commit=False)
				pub.user_publisher = request.user
				errors = self.saveAuteurs(pr_auteur, co_auteurs, pub)
				for e in errors:
					form.add_error(None, e)
				if len(errors) == 0:
					return myredirect('Biblio:information')

		context = self.getContext()
		context['form'] = form
		context['auteurs'] = auteursList
		return render(request, self.tmp_add_publication, context)

	def get(self, request):
		return self.defaultPage(request)
	
	def post(self, request):
		return self.defaultPage(request)

#la fonction sert a modifier un block d'informations (une formulaire precise)
#le parametre id sert a definir une formulaire precise chaque formulaire a un identificateurs precise definie par django
@login_required(login_url='/login/')
def update(request, f_id):
	def saveAuteurs(pr_auteur, co_auteurs, pub):
		errors = []
		try:
			json_auteurs = json.loads(co_auteurs)
			ids = [int(x['id']) for x in json_auteurs]
			prauteur = AuteurModel.objects.filter(id = pr_auteur)
			coauteurs = AuteurModel.objects.filter(id__in=ids)
			if not prauteur.exists():
				errors.append('pr.auteur')
			if not coauteurs.exists():
				errors.append('co.auteur')
			if pr_auteur in co_auteurs:
				errors.append('pr.auteur = co.auteur')
			if len(errors) != 0:
				return errors

			a = AuteurRelationsModel.objects.filter(pub = pub)
			a.delete()
			pub.save()
			AuteurRelationsModel(auteur = prauteur[0], pub = pub, auteur_type=0).save()
			for item in coauteurs:
			 	AuteurRelationsModel(auteur = item, pub = pub, auteur_type=1).save()
			return errors
		except:
			errors.append("error")
			return errors
	#get
	formulaire = PublicationModel.objects.get(id = f_id)
	form = PublicationModelForm(instance = formulaire)

	if request.POST:
		form = PublicationModelForm(request.POST, request.FILES, instance = formulaire)
		pr_auteur = request.POST.get('pr_auteur')
		co_auteurs = request.POST.get('co_auteurs')
		if form.is_valid():         
			pub = form.save(commit=False)
			errors = saveAuteurs(pr_auteur, co_auteurs, pub)
			for e in errors:
				form.add_error(None, e)
			if len(errors) == 0:
				return myredirect('Biblio:information')
	
	context ={

		"biblio_active" : "active",
		"form" : form,
		"title_section" : "Bibliotheque",
		"auteurs" : AuteurModel.objects.all(),
		'f_id' : f_id
		
	 }
		 
	return render(request,'Biblio/ajouter.html', context)

class GetUpdateAuteurs(View):
	def getAsJson(self, type, data):
		response_data = {}
		response_data[type] = data
			
		return HttpResponse(
			json.dumps(response_data),
			content_type='application/json'
		)

	def get(self, request, id):
		result = []
		auteurs = AuteurRelationsModel.objects.filter(pub = id)
		for item in auteurs:
			aut = item.auteur
			result.append({
				'id' : aut.id, 
				'auteur' : aut.name, 
				'type' : item.auteur_type
			})
		print(result)
		return self.getAsJson('auteurs', result)




def searchAuteur(auteur):
	auteurs = AuteurModel.objects.filter(name__contains = auteur)
	pubs = AuteurRelationsModel.objects.filter(auteur__in = auteurs)
	pubs = [item.pub for item in pubs]
	return pubs
			
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

		auteurs = AuteurRelationsModel.objects.all().values('auteur').distinct()
		auteurs = [int(x['auteur']) for x in auteurs]
		auteurs = AuteurModel.objects.filter(id__in = auteurs)
		auteurs = [x.name for x in auteurs]

		data = auteurs

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

