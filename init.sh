superUser="from Account.models import "
superUser+="(UserAccount, DoctorantModel, EncadrantModel);"
superUser+="from django.contrib.auth.models import Group;"


superUser+="group0 = Group.objects.get(name = 'encadrant');"
superUser+="group1 = Group.objects.get(name = 'doctorant');"
superUser+="group2 = Group.objects.get(name = 'admin');"

# user 1
superUser+="omar = UserAccount.objects.create_user(email='omar.jed@uit.ac.ma', first_name = 'omar', last_name = 'jed',group='doctorant', password='ase123@$');"

superUser+="ayoub = UserAccount.objects.create_user(email='ayoub.benhamou@uit.ac.ma',first_name = 'ayoub', last_name = 'ben hamou',group='doctorant', password='ase123@$');"

superUser+="salma = UserAccount.objects.create_user(email='mohammed.aminetajioue@uit.ac.ma',first_name = 'mohammed', last_name = 'Amine tajioue',group='encadrant', password='ase123@$');"

superUser+="sara = UserAccount.objects.create_user(email='sara.hsaini@uit.ac.ma',first_name = 'sara', last_name = 'hasaini',group='encadrant', password='ase123@$');"

superUser+="omar.is_signed = True;"
superUser+="ayoub.is_signed = True;"
superUser+="salma.is_signed = True;"
superUser+="sara.is_signed = True;"

superUser+="omar.save();"
superUser+="ayoub.save();"
superUser+="salma.save();"
superUser+="sara.save();"

superUser+="EncadrantModel(user = salma).save();"
superUser+="EncadrantModel(user = sara).save();"

superUser+="DoctorantModel(user = omar, apogee = '18005544', cin = 'GM215420').save();"
superUser+="DoctorantModel(user = ayoub, apogee = '18005544', cin = 'GM215420').save();"



#echo "$superUser"
py manage.py shell -c "$superUser"
py manage.py runserver
