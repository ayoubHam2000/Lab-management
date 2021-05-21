## commands ##

pip install virtualenv
virtualenv env_name
activate
deactivate
djan\Scripts\activate

## github
git init 
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/ayoubHam2000/Lab-management-.git
git push -u origin main

git log --oneline
git checkout -b [branch] [6e559cb]

git branch -m ayoub Main
git fetch origin
git branch -u origin/Main Main
git remote set-head origin -a

-- Create the branch on your local machine and switch in this branch :
$ git checkout -b [name_of_your_new_branch]
-- Push the branch on github :
$ git push origin [name_of_your_new_branch]
-- You can see all the branches created by using :
$ git branch -a
-- Delete a branch on your local filesystem :
$ git branch -d [name_of_your_new_branch]
-- Delete the branch on github :
$ git push origin :[name_of_your_new_branch]

## django ##

pip install django
django-admin startproject djcrm .
py manage.py migrate => sync the models with the data base
py manage.py makemigrations => create the shema
py manage.py migrate --run-syncdb
py manage.py createsuperuser
py manage.py dbshell
py manage.py shell
py manage.py startapp appName

py manage.py migrate your_app zero
py manage.py migrate --fake <app-name> zero
py manage.py makemigrations <app-name>
py manage.py migrate <app-name>

## sqlite ##
ctrl + shift + p
open database


## models
    # SOURCE_CHOICES = (
    #     ('Youtube', 'Youtube'),
    #     ('Google', 'Google'),
    #     ('Newsletter', 'Newsletter'),
    # )
CharField(choices=SOURCE_CHOICES, max_length=100)
IntegerField(default = 0)
BooleanField(default = False)
ImageField(blank = True, null = True)
FileField(blank = True, null = True)

-> lead models

## Model manager

- to access the medel manager
Car.objects

- Using the manager we can create new cars
Car.obects.create(make = "BWM", model = "X5")

- Using the manager we can query the database
Car.objects.all()
Car.objects.filter(make = 'Audi')
Car.objects.filter(year__gt = 2016)

## Other

-- get all users
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> User.objects.all()

>>> from leads.models import Agent
>>> Agent.objects.create(user = admin_user)

>>> Agent.objects.get(user__email = "a@gmail.com")


## scss
https://www.accordbox.com/blog/how-use-scss-sass-your-django-project-python-way/

**install**
py -m pip install django_compressor
py -m pip install django-libsass

**add to settings**

INSTALLED_APPS = [
    'compressor',
]

STATIC_URL = '/static/'
STATIC_ROOT = '/static/'
COMPRESS_ROOT = BASE_DIR / 'static'

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

**Use Like**
{% load compress %}
{% load static %}

{% compress css %}
    <link type="text/x-scss" href="{% static 'scss/style.scss' %}" rel="stylesheet" media="screen">
{% endcompress %}



## User Log IN

*urls*
from django.contrib.auth.views import LoginView
path('login', LoginView.as_view(), name = 'login')
templates\registration\login.html
*settings*
LOGIN_REDIRECT_URL = '/'
*vars*
request.user.is_authenticated
request.user.username


#### Emails
from django.core.mail import send_mail
send_mail(
    'Virivication Email',
    'click this link to virify your email',
    'noreply@uit.ac.ma',
    [dist],
    fail_silently=False,
)

from dotenv import dotenv_values
config = dotenv_values(".env")
EMAIL_HOST = config['EMAIL_HOST']
EMAIL_HOST_USER = config['EMAIL_HOST_USER']
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_PASSWORD = config['EMAIL_HOST_PASSWORD']
DEFAULT_FROM_EMAIL = config['EMAIL_HOST_USER']



##### Token
PASSWORD_RESET_TIMEOUT_DAYS = 1

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
class AppTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, member, timestamp):
        return (
            text_type(member.email) + text_type(timestamp)
        )
token_generator = AppTokenGenerator()

//use it in view
link = reverse('Account:memberRegister', kwargs={
            'uidb64' : uidb64,
            'token' : token_generator.make_token(member),
        })
token_generator.check_token(member, token)


## user image profile
py -m pip install pillow
MEDIA_ROOT = BASE_DIR
