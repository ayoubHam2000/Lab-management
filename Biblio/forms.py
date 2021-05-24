from django import forms
from django.forms import ModelForm
#from django.forms.models import ModelForm
from .models import Formulaire,Auteur,Mot_cle,Base_Bibliographique,Journal

from Utils.const import *


class FormulaireForm(ModelForm):
	#type_pub = forms.ChoiceField(choices = TYPE_PUB)
	#theme = forms.ChoiceField(choices = THEME)
	class Meta:
		model = Formulaire
		fields = [
			'title','type_pub','issn','volume','pr_page','der_page',
			'publisher','doi','theme','date','fichier'
		]

class Mot_CleForm(ModelForm):
	class Meta:
		model = Mot_cle
		fields = [
			'mot_cle'
		]

class AuteurForm(ModelForm):
	class Meta:
		model = Auteur
		fields = [
			'auteur','auteur_type'
		]

class BibliographiqueForm(ModelForm):
	#name_base = forms.ChoiceField(choices = BASE_BIBLIO)
	class Meta:
		model = Base_Bibliographique
		fields = [
			'name_base'
		]

class JournalForm(ModelForm):
	class Meta:
		model = Journal
		fields = [
			'name_jrnl'
		]
