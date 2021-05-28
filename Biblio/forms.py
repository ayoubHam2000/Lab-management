from django import forms
from django.forms import ModelForm
#from django.forms.models import ModelForm
from .models import Formulaire



class FormulaireForm(ModelForm):
	class Meta:
		model = Formulaire
		fields = [
			'pr_auteur','titre','co_auteur','type_pub','doi','volume','citation','pr_page','der_page','date','journal','issn',
			'publisher','fichier'
		]
	def __init__(self, *args, **kwargs):
		super(FormulaireForm , self).__init__(*args, **kwargs)
		self.fields['co_auteur'].widget.attrs.update({
			'id': 'co_auteur_input',})

	# clean_issn nous permet de controler issn
	def clean_issn(self):
		issn = self.cleaned_data.get('issn')
		if not issn.isnumeric():
			return forms.ValidationError("Field must be a number")
		return issn