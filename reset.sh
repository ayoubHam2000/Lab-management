
rm -r biblio/migrations
rm -r Admin/migrations
rm db.sqlite3


py manage.py migrate
py manage.py migrate --run-syncdb

echo 'Add groups'
py manage.py shell -c "from django.contrib.auth.models import Group; Group.objects.create(name='doctorant')"
py manage.py shell -c "from django.contrib.auth.models import Group; Group.objects.create(name='encadrant')"
py manage.py shell -c "from django.contrib.auth.models import Group; Group.objects.create(name='admin')"


echo 'Create SuperUSer'
superUser="from Admin import User;"
superUser+="User.objects.create_user"
superUser+="('omar', 'a@gmail.com', '123456789');"

py manage.py shell -c "$superUser"

py manage.py createsuperuser