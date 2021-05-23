from django.urls import path

from .views import (
    Ajouter,
    pagebib,
)

app_name = 'Biblio'

urlpatterns = [
    path('add', Ajouter, name = "formulaire"),
    path('info', pagebib, name = "information"),
]