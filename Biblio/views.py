from django.shortcuts import render, HttpResponse
from django.views import View
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage

from django.db.models import Q


from .models import Formulaire

from .forms import FormulaireForm

from Utils.functions import myredirect

def Ajouter(request):
	form = FormulaireForm() 
	if request.POST :
		form = FormulaireForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return myredirect('Biblio:information')
			
	
	
	#form = FormulaireForm() 

	context ={
		"biblio_active" : "active",
		"form" : form,
		"title_section" : "Bibliotheque"
	 }
		 
	return render(request,'Biblio/telechargement.html', context)


#la fonction sert a modifier un block d'informations (une formulaire precise)
#le parametre id sert a definir une formulaire precise chaque formulaire a un identificateurs precise definie par django
def update(request, f_id):
	#get
	formulaire = Formulaire.objects.get(id = f_id)
	form = FormulaireForm(instance = formulaire)

	if request.POST:
		form = FormulaireForm(request.POST, request.FILES, instance = formulaire)
		if form.is_valid():         
			form.save()
			return myredirect('Biblio:information')
	
	context ={

		"biblio_active" : "active",
		"form" : form,
		"title_section" : "Bibliotheque"
	 }
		 
	return render(request,'Biblio/telechargement.html', context)

def searchAuteur(auteur):
	listAuteurs = []
	formulaires = Formulaire.objects.all()
	for item in formulaires:
		if item.pr_auteur == auteur or auteur in item.co_auteur.split(","):
			listAuteurs.append(item)
	return listAuteurs
			
#cette fonction sert a la recherche (a partir de la barre de recherche )
def pagebib(request):
	searchType = request.GET.get("searchType")
	search = request.GET.get("mySearch")

	if search == None:            
		formulaires = Formulaire.objects.all()
	else:
		if searchType == 'auteur':
			formulaires = searchAuteur(search)
		if searchType == 'titre':
			formulaires = Formulaire.objects.filter(titre = search)
		if searchType == 'journal':
			formulaires = Formulaire.objects.filter(journal = search)
			
	context ={
		
		"biblio_active" : "active",
		"formulaires" : formulaires,
		"title_section" : "Bibliotheque"
	}

	if len(formulaires) == 0:   # cette partie si on n'a aucune formulaire 
		return render(request,'Biblio/empty_bib.html',context)
	

	return render(request,'Biblio/page_biblio.html', context)



def deleteF(request, id_F):
	if request.POST:
		formulaire = Formulaire.objects.filter(id = id_F)
		formulaire.delete()
		return myredirect('Biblio:information')

import json     
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
		theList = Formulaire.objects.order_by().values(type).distinct()
		data = []
		for item in theList:
			data = data + [item.get(type)]
		return self.getAsJson(type, data)

	def getListAuteur(self):
		s_type = ['pr_auteur', 'co_auteur'] 

		pr_auteurs = Formulaire.objects.order_by().values(s_type[0]).distinct()
		co_auteurs = Formulaire.objects.order_by().values(s_type[1]).distinct()

		data1 = []
		for item in pr_auteurs:
			theList = [item.get(s_type[0])]
			data1 = data1 + theList
		
		data2 = []
		for item in co_auteurs:
			#it has to be at least one co_auteur
			theList = item.get(s_type[1]).split(",")
			data2 = data2 + theList[:len(theList) - 1]

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
		print(type)
		if type == None:
			return self.pageRecherche(request)
		else:
			if type == 'auteur':
				return self.getListAuteur()
			return self.getList(type)
			
		
