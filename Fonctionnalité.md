## Fonctionnalité 
**add users**

*usertype*
doctorant
encadrant
admin
superuser

*bib*
can add formulaire
can delete formulaire
can modify formulaire
can view formulaire
can search formulaire by(auteur, issn, doi, titre, journal)
search autocompletion

*post*
can add post (text and image)
can delete post
can't modifiy post
can add comment
can't delete of modify comment

*list members*
    **doctorant**
    can see mon_encadrant, mes co_encadrants, doctorants with the same encadrant
    **encadrant**
    can see mes_doctorants, mes_doctorant as co.encadrant, co_encadrand of mes doctorant

*account(menu)*
can change all info
can change password

*addmember(menu)*
access account
add relations
activate deactivate account
activate deactivate admin

*addmember*
add encadrant
add doctorant
add admin
add relations
deactivate activate account
deactivate activate admin
delete account
can view the status of the user(not signin, active, not active)
can search by email
can sort by email, date, status, usertype(doc, enc, admin)
can't delete superadmin

*relation*
can add encadrant to doctorant
can add co_encadrant to doctorant
can add doctorant to encadrant 
can add doctorant to co_encadrant
can't add the same relation (relation between (encadrant, co_encadrant) and doctorant)
    ->                  doctorant   encadrant   relationtype
    -> relation like    omar        salma       encadrant
    -> is the same as   omar        salma       co_encadrant
can't add relation doctorant to doctorant
can't add relation encadrant to encadrant
can't add relation to doctorant already has encadrant


*doctorant*
can add formulaire
can modify formulaire
can modify profile info
can post
can delete his post
can comment
can change password
can't delete formulaire
can't modify these
can't access addmember


*encadrant*
can delete formulaire
can change these (only mes doctorants)
can change users profile info (only mes doctorants)


*admin*
can access addmember
can add doctorant
can add encadrant
can add relation to docorants and encadrant
can change these (all doctorant)
can change password (all doctorant and encadrant)
can delete encadrant doctorant
can deactivate activate account (encadrant, doctorat)
can't access admin (menu, delete)
can't add admin

    -> can't change password of admin
    -> can't add relations to admin
    -> can't access account admin
    -> can't actiivate deactivate admin
    -> can't delete admin



*super admin*
can add admin
can deactivate/activate admin 
can add relations to any user
can change password and profile info to all users
can access the menu
basically he can do anything but he can't delete himself