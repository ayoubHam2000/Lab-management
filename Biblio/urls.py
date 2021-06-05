from django.urls import path

from .views import (
    AddPublication,
    pagebib,
    update,
    searchbib,
    deleteF,
    AuteurViw,
    GetUpdateAuteurs
)

app_name = 'Biblio'

urlpatterns = [
    path('add/', AddPublication.as_view(), name = "formulaire"),
    path('info/', pagebib, name = "information"),
    path('auteurs/', AuteurViw.as_view(), name = "auteurs"),
    path('auteurs/getAuteurs/<int:id>', GetUpdateAuteurs.as_view(), name = "updateAuteurs"),
    path('auteurs/<str:action>/', AuteurViw.as_view(), name = "auteur_actions"),
    path('update/<int:f_id>/', update, name = "update"),
    path('searchbib/', searchbib.as_view(), name = "search_bib"),
    path('searchbib/<type>/', searchbib.as_view(), name = "search_bib"),
    path('info/delete/<int:id_F>/', deleteF, name = 'deleteFormulaire'),
    #path(r'^searchbib/(?P<type>\d+)', searchbib.as_view(), name = "search_bib"),
    #path('searchbib/auteur', searchbib.as_view(), name = "search_bib"),
    
   ]