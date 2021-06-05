from django.contrib import admin

from .models import PublicationModel, AuteurModel


admin.site.register(PublicationModel)
admin.site.register(AuteurModel)