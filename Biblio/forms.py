from django.forms import fields, forms
from django.forms.models import ModelForm
from biblio.models import formulaire

class formulaireForm(ModelForm):
    class Meta:
        model = formulaire
        fields = [
            'name','Email','Filiere','photo'
        ]