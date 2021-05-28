from django.shortcuts import redirect
from django.urls import reverse
import time
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
import os

def myredirect(url):
    return redirect(reverse(url))


def current_milli_time():
    return round(time.time() * 1000)

def getFileName(path):
    return os.path.basename(path)

class AppTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, member, timestamp):
        return (
            text_type(member.email) + text_type(timestamp)
        )
token_generator = AppTokenGenerator()


def deleteUser(user):
    email = user.email
    doctorantRelation = Account.models.DoctorantRelation.objects.filter(email = 'email')
    doctorantRelation.delete()
    user.delete()
