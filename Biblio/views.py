from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage


from .models import Formulaire,Auteur,Mot_cle,Base_Bibliographique,Journal

from .forms import FormulaireForm,Mot_CleForm,AuteurForm,BibliographiqueForm,JournalForm

def Ajouter(request):
    formF = FormulaireForm() 
    formJ = JournalForm()
    formA = AuteurForm()
    formMC = Mot_CleForm()
    formB = BibliographiqueForm()
    if request.POST :
        formF = FormulaireForm(request.POST , request.FILES)
        formJ = JournalForm(request.POST)
        formA = AuteurForm(request.POST)
        formB = BibliographiqueForm(request.POST)
        formMC = Mot_CleForm(request.POST)

        
        if formf.is_valid() and formJ.is_valid() and formA.is_valid() and formB.is_valid() and formMC.is_valid() :
            formF.save()
            formJ.save()
            formA.save()
            formB.save()
            formMC.save()
    
    formF = FormulaireForm() 
    formJ = JournalForm()
    formA = AuteurForm()
    formMC = Mot_CleForm()
    formB = BibliographiqueForm()

    froms = [formF, formJ, formA, formB, formMC]
    context ={

        "formF" : formF,
        "formJ" : formJ,
        "formA" : formA,
        "formB" : formB,
        "formMC" : formMC

     }
         
    return render(request,'Biblio/telechargement.html', context)




def pagebib(request):

    formulaires = Formulaire.objects.all()
    mot_cles = Mot_cle.objects.all()
    #journals = Journal.object.all()
    base_biblios = Base_Bibliographique.objects.all()
    auteurs = Auteur.objects.all()

    context ={

        "formulaires" : formulaires,
        "mot_cles" : mot_cles,
        #"journals" : journals,
        "base_biblios" : base_biblios,
        "auteurs" : auteurs
    }

    return render(request,'Biblio/page_biblio.html', context)
 