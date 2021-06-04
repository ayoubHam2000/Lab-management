
rm -r Account/migrations
rm -r Biblio/migrations
rm -r Compt/migrations
rm db.sqlite3


#py manage.py migrate
py manage.py migrate --run-syncdb

echo 'Add groups'
py manage.py shell -c "from django.contrib.auth.models import Group; Group.objects.create(name='doctorant')"
py manage.py shell -c "from django.contrib.auth.models import Group; Group.objects.create(name='encadrant')"
py manage.py shell -c "from django.contrib.auth.models import Group; Group.objects.create(name='admin')"
py manage.py shell -c "from django.contrib.auth.models import Group; Group.objects.create(name='superadmin')"


echo 'Create SuperUSer'
superUser="from Account.models import UserAccount;"
superUser+="user = UserAccount.objects.create_superuser"
superUser+="('ayoub@gmail.com', 'ayoub', 'ben hamou', 'ase123@$');"

py manage.py shell -c "$superUser"

py manage.py runserver
