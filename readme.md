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