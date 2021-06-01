from django.shortcuts import redirect
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
    def _make_hash_value(self, member, timestamp):
        return (
            text_type(member.email) + text_type(timestamp)
        )
token_generator = AppTokenGenerator()


def deleteUser(user):
    #email = user.email
    #doctorantRelation = Account.models.DoctorantRelation.objects.filter(email = 'email')
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
