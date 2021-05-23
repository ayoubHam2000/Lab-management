from django.forms import fields, forms
from django.forms.models import ModelForm
from .models import Formulaire

class FormulaireForm(ModelForm):
    class Meta:
        model = Formulaire
        fields = [
            'name','email','filiere','photo'
        ]