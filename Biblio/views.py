from .forms import formulaireForm
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage


from .models import formulaire

def Ajouter(request):
    form = formulaireForm()
    if request.POST :
        form = formulaireForm(request.POST , request.FILES)
        if form.is_valid() :
            form.save()
    
        form = formulaireForm()
    
    formulaires = formulaire.objects.all()
    context ={
        "formulaires" : formulaires,
        "form" : form
     }
         
    return render(request,'Biblio/telechargement.html', context)