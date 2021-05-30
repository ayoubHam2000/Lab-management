from django import forms
from django.forms import ModelForm
#from django.forms.models import ModelForm
from .models import Formulaire



class FormulaireForm(ModelForm):
	volume = forms.CharField(max_length=50)
	pr_page = forms.CharField(max_length=50)
	der_page = forms.CharField(max_length=50)
	citation = forms.CharField(max_length=50)
	class Meta:
		model = Formulaire
		fields = '__all__'
        #exclude = ['user']

	# clean_issn nous permet de controler issn
	def clean_issn(self):
		issn = self.cleaned_data.get('issn')
		if not issn.isnumeric():
			return forms.ValidationError("Field must be a number")
		return issn