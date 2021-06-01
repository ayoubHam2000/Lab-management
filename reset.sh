
rm -r Account/migrations
rm -r Biblio/migrations
rm -r Compt/migrations
rm db.sqlite3


py manage.py migrate
py manage.py migrate --run-syncdb

echo 'Add groups'
py manage.py shell -c "from django.contrib.auth.models import Group; Group.objects.create(name='doctorant')"
py manage.py shell -c "from django.contrib.auth.models import Group; Group.objects.create(name='encadrant')"
py manage.py shell -c "from django.contrib.auth.models import Group; Group.objects.create(name='admin')"
py manage.py shell -c "from django.contrib.auth.models import Group; Group.objects.create(name='superadmin')"


echo 'Create SuperUSer'
superUser="from Account.models import UserAccount, MemberModel;"
superUser+="user = UserAccount.objects.create_superuser"
superUser+="('omar@gmail.com', 'omar', 'omar', 'jed', 'omarjed');"
superUser+="from django.contrib.auth.models import Group;"
superUser+="from Account.models import EncadrantModel;"
superUser+="group = Group.objects.get(name = 'superadmin');"
superUser+="user.groups.add(group);"

superUser+="MemberModel(user = user, email = user.email, userType = 3).save();"
superUser+="EncadrantModel(user = user).save();"

py manage.py shell -c "$superUser"

py manage.py runserver
