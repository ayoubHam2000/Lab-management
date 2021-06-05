from django.contrib import admin

from .models import PublicationModel, AuteurModel, AuteurRelationsModel


admin.site.register(PublicationModel)
admin.site.register(AuteurModel)
admin.site.register(AuteurRelationsModel)