from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage


from .models import Formulaire

from .forms import FormulaireForm

def Ajouter(request):
    form = FormulaireForm() 
    if request.POST :
        form = FormulaireForm(request.POST , request.FILES)
        
        if form.is_valid():
            form.save()
    
    form = FormulaireForm() 

    context ={
        "form" : form
     }
         
    return render(request,'Biblio/telechargement.html', context)




def pagebib(request):

    formulaires = Formulaire.objects.all()
    
    context ={

        "formulaires" : formulaires
    }

    return render(request,'Biblio/page_biblio.html', context)
 