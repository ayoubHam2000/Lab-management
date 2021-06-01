superUser="from Account.models import "
superUser+="(UserAccount, MemberModel, DoctorantModel, EncadrantModel, MemberModel);"
superUser+="from django.contrib.auth.models import Group;"


superUser+="group0 = Group.objects.get(name = 'encadrant');"
superUser+="group1 = Group.objects.get(name = 'doctorant');"
superUser+="group2 = Group.objects.get(name = 'admin');"

# user 1
superUser+="omar = UserAccount.objects.create_user(email='omar@gmail.com', username='user_1', first_name='omar', last_name='jed', password='omarjed');"

superUser+="rachid = UserAccount.objects.create_user(email='rachid@gmail.com', username='user_2', first_name='rachid', last_name='ben hamou', password='ase123@$');"

superUser+="sara = UserAccount.objects.create_user(email='sara@gmail.com', username='user_3', first_name='sara', last_name='Hsaini', password='ase123@$');"

superUser+="salma = UserAccount.objects.create_user(email='salma@gmail.com', username='user_4', first_name='salma', last_name='Azzouzi', password='ase123@$');"

superUser+="omar.save();"
superUser+="rachid.save();"
superUser+="sara.save();"
superUser+="salma.save();"

superUser+="EncadrantModel(user = salma).save();"
superUser+="EncadrantModel(user = sara).save();"

superUser+="DoctorantModel(user = omar, apogee = '18005544', cin = 'GM215420').save();"
superUser+="DoctorantModel(user = rachid, apogee = '18005544', cin = 'GM215420').save();"

superUser+="MemberModel(user = omar, email = omar.email, userType = 1).save();"
superUser+="MemberModel(user = rachid, email = rachid.email, userType = 1).save();"
superUser+="MemberModel(user = sara, email = sara.email, userType = 0).save();"
superUser+="MemberModel(user = salma, email = salma.email, userType = 0).save();"

superUser+="omar.groups.add(group1);"
superUser+="rachid.groups.add(group1);"
superUser+="sara.groups.add(group0);"
superUser+="salma.groups.add(group0);"



#echo "$superUser"
py manage.py shell -c "$superUser"
py manage.py runserver
