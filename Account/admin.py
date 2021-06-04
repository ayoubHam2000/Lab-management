from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    DoctorantModel,
    UserAccount,
    EncadrantModel,
    RelationModel,
)

class AccountAdmin(UserAdmin):
    list_displayed = ('email', 'username', 'date_joined', 'last_login', 'is_admin')
    searsh_fields = ('email', 'username')
    readonly_fields = ('id', 'date_joined', 'last_login')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class RelationModelAdmin(admin.ModelAdmin):
    list_display = ('__str__', '_relationType',)

admin.site.register(DoctorantModel)
admin.site.register(EncadrantModel)
admin.site.register(RelationModel, RelationModelAdmin)
admin.site.register(UserAccount, AccountAdmin)
