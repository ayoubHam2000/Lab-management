from django.shortcuts import redirect, Http404
from django.urls import reverse
import time
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
import os

from .const import *

def myredirect(url):
    return redirect(reverse(url))


def current_milli_time():
    return round(time.time() * 1000)

def getFileName(path):
    return os.path.basename(path)

def getTimeFormat(date):
    return date.strftime(DATE_FORMAT)

class AppTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user.email) + text_type(timestamp)
        )
token_generator = AppTokenGenerator()


def deleteUser(user):
    #email = user.email
    #doctorantRelation = Account.models.RelationModel.objects.filter(email = 'email')
    #doctorantRelation.delete()
    user.delete()

def getUserTypeName(t):
    if t == 0:
        return 'Encadrant'
    if t == 1:
        return 'Doctorant'
    if t == 2:
        return 'Admin'
    if t == 3:
        return 'Admin'

def getUserTypeFromGroup(user):
    group = user.groups.all()[0].name
    if group == 'admin':
        return 2
    if group == 'superadmin':
        return 2
    if group == 'doctorant':
        return 1
    if group == 'encadrant':
        return 0
    return 1


def getUserTypeNameFromGroup(user):
    group = user.groups.all()[0].name
    if group == 'admin':
        return 'Responsable'
    if group == 'superadmin':
        return 'Administrateur'
    if group == 'doctorant':
        return 'Doctorant'
    if group == 'encadrant':
        return 'Encadrant'
    return 1

def get_object_or_404(Model, id):
    try:
        instance = Model.objects.get(id = id)
        return instance
    except Model.DoesNotExist:
        raise Http404("No MyModel matches the given query.")
        #return render_to_response(P_404)
