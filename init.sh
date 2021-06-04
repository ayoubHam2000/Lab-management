superUser="from Account.models import "
superUser+="(UserAccount, DoctorantModel, EncadrantModel);"
superUser+="from django.contrib.auth.models import Group;"


superUser+="group0 = Group.objects.get(name = 'encadrant');"
superUser+="group1 = Group.objects.get(name = 'doctorant');"
superUser+="group2 = Group.objects.get(name = 'admin');"

# user 1
superUser+="omar = UserAccount.objects.create_user(email='omar@gmail.com', first_name = 'omar', last_name = 'jed',group='doctorant', password='omarjed');"

superUser+="rachid = UserAccount.objects.create_user(email='rachid@gmail.com',first_name = 'rachid', last_name = 'ben hamou',group='doctorant', password='ase123@$');"

superUser+="salma = UserAccount.objects.create_user(email='salma@gmail.com',first_name = 'salma', last_name = 'azzouzi',group='encadrant', password='ase123@$');"

superUser+="sara = UserAccount.objects.create_user(email='sara@gmail.com',first_name = 'sara', last_name = 'hasaini',group='encadrant', password='ase123@$');"


superUser+="omar.save();"
superUser+="rachid.save();"
superUser+="sara.save();"
superUser+="salma.save();"

superUser+="EncadrantModel(user = salma).save();"
superUser+="EncadrantModel(user = sara).save();"

superUser+="DoctorantModel(user = omar, apogee = '18005544', cin = 'GM215420').save();"
superUser+="DoctorantModel(user = rachid, apogee = '18005544', cin = 'GM215420').save();"



#echo "$superUser"
py manage.py shell -c "$superUser"
py manage.py runserver
