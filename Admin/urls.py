from django.urls import path

from .views import (
    AdminAddMember
)

app_name = 'Admin'

urlpatterns = [
    path('', AdminAddMember.as_view(), name = "addMember")
]