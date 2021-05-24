from django import forms
from django.forms import ModelForm
#from django.forms.models import ModelForm
from .models import Formulaire



class FormulaireForm(ModelForm):
	class Meta:
		model = Formulaire
		fields = [
			'titre','type_pub','doi','volume','pr_page','der_page','date','pr_auteur','co_auteur','journal','issn',
			'publisher','fichier'
		]
