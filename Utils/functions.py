from django.shortcuts import redirect
from django.urls import reverse
import time
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

def myredirect(url):
    return redirect(reverse(url))

def current_milli_time():
    return round(time.time() * 1000)


class AppTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, member, timestamp):
        return (
            text_type(member.email) + text_type(timestamp)
        )
token_generator = AppTokenGenerator()