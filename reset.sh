
rm -r Account/migrations
rm -r Admin/migrations
rm db.sqlite3


py manage.py migrate
py manage.py migrate --run-syncdb

echo 'Add groups'
py manage.py shell -c "from django.contrib.auth.models import Group; Group.objects.create(name='doctorant')"
py manage.py shell -c "from django.contrib.auth.models import Group; Group.objects.create(name='encadrant')"
py manage.py shell -c "from django.contrib.auth.models import Group; Group.objects.create(name='admin')"


echo 'Create SuperUSer'
superUser="from Account.models import UserAccount;"
superUser+="user = UserAccount.objects.create_superuser"
superUser+="('ayoub@gmail.com', 'ayoub', 'ayoub', 'ben hamou', 1, 'ase123@$');"
superUser+="from django.contrib.auth.models import Group;"
superUser+="group = Group.objects.get(name = 'admin');"
superUser+="user.groups.add(group);"

py manage.py shell -c "$superUser"

py manage.py runserver