from django.urls import path

from .views import (
    AdminAddMember,
    AdminAddMember_cont,
    AdminAddMember_test,
)

app_name = 'Admin'

urlpatterns = [
    path('', AdminAddMember.as_view(), name = "addMember"),
    path('contenu/', AdminAddMember_cont.as_view(), name = "contenu"),
    path('test/', AdminAddMember_test.as_view(), name = "test"),

]

