from django.urls import path

from .views import (
    AddPublication,
    pagebib,
    update,
    searchbib,
    deleteF,
)

app_name = 'Biblio'

urlpatterns = [
    path('add/', AddPublication.as_view(), name = "formulaire"),
    path('info/', pagebib, name = "information"),
    path('update/<int:f_id>/', update, name = "update"),
    path('searchbib/', searchbib.as_view(), name = "search_bib"),
    path('searchbib/<type>/', searchbib.as_view(), name = "search_bib"),
    path('info/delete/<int:id_F>/', deleteF, name = 'deleteFormulaire'),
    #path(r'^searchbib/(?P<type>\d+)', searchbib.as_view(), name = "search_bib"),
    #path('searchbib/auteur', searchbib.as_view(), name = "search_bib"),
    
   ]