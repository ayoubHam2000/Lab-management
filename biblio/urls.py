from django.urls import path
from .views import Ajouter

app_name = 'biblio'

urlpatterns = [
    path('', Ajouter, name = "formulaire"),
]