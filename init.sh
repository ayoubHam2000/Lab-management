superUser="from Account.models import "
superUser+="(UserAccount, MemberModel, DoctorantModel, EncadrantModel, MemberModel);"
superUser+="from django.contrib.auth.models import Group;"


superUser+="group0 = Group.objects.get(name = 'encadrant');"
superUser+="group1 = Group.objects.get(name = 'doctorant');"
superUser+="group2 = Group.objects.get(name = 'admin');"

# user 1
superUser+="ayoub = UserAccount.objects.create_user(email='ayoub@gmail.com', username='user_1', first_name='ayoub', last_name='ben hamou', password='ase123@$');"

superUser+="rachid = UserAccount.objects.create_user(email='rachid@gmail.com', username='user_2', first_name='rachid', last_name='ben hamou', password='ase123@$');"

superUser+="sara = UserAccount.objects.create_user(email='sara@gmail.com', username='user_3', first_name='sara', last_name='Hsaini', password='ase123@$');"

superUser+="salma = UserAccount.objects.create_user(email='salma@gmail.com', username='user_4', first_name='salma', last_name='Azzouzi', password='ase123@$');"

superUser+="ayoub.save();"
superUser+="rachid.save();"
superUser+="sara.save();"
superUser+="salma.save();"

superUser+="EncadrantModel(user = salma).save();"
superUser+="EncadrantModel(user = sara).save();"

superUser+="DoctorantModel(user = ayoub, apogee = '18005544', cin = 'GM215420').save();"
superUser+="DoctorantModel(user = rachid, apogee = '18005544', cin = 'GM215420').save();"

superUser+="MemberModel(user = ayoub, email = ayoub.email, userType = 1).save();"
superUser+="MemberModel(user = rachid, email = rachid.email, userType = 1).save();"
superUser+="MemberModel(user = sara, email = sara.email, userType = 0).save();"
superUser+="MemberModel(user = salma, email = salma.email, userType = 0).save();"

superUser+="ayoub.groups.add(group1);"
superUser+="rachid.groups.add(group1);"
superUser+="sara.groups.add(group0);"
superUser+="salma.groups.add(group0);"



#echo "$superUser"
py manage.py shell -c "$superUser"
py manage.py runserver
