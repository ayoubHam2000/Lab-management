from django import forms
from django.forms import ModelForm
#from django.forms.models import ModelForm

from .models import (
	PublicationModel,
)


class PublicationModelForm(ModelForm):
	volume = forms.CharField(max_length=50)
	pr_page = forms.CharField(max_length=50)
	der_page = forms.CharField(max_length=50)
	citation = forms.CharField(max_length=50)
	class Meta:
		model = PublicationModel
		fields = '__all__'
		exclude = ('user_publisher',)
		labels = {
			'pr_auteur' : "Premiere Auteur*",
			'co_auteur' : "Co.Auteur*",
			"titre":"Titre *",
            "type_pub": "Type publication*",
            "doi": "DOI*",
            "volume": "Volume",
            "pr_page": "Premiere page",
			"der_page":"Derniere page",
            "citation": "Nomber citation",
            "date": "Date",
            "journal": "Journal*",
            "issn": "ISSN*",
            "publisher": "Publisher",
            "fichier": "Fichier*",
        }

	# clean_issn nous permet de controler issn
	def clean_issn(self):
		issn = self.cleaned_data.get('issn')
		if not issn.isnumeric():
			return forms.ValidationError("Field must be a number")
		return issn

