from django.db import models

from Utils.const import *


class Base_Bibliographique(models.Model):
	name_base = models.CharField(max_length=MAXCHAR)


class Journal(models.Model):
	base_bibliographique = models.ForeignKey(Base_Bibliographique, on_delete= models.CASCADE)
	name_jrnl = models.CharField(max_length=MAXCHAR)

def get_file_path(instance, filename):
	return f'files/{instance.id}/{filename}'

class Formulaire(models.Model):
	title =models.CharField(max_length=MAXCHAR)
	type_pub = models.CharField(max_length=MAXCHAR)
	issn = models.IntegerField(max_length=ISSN_MAX)
	volume = models.IntegerField(max_length=VOLUME_MAX,blank=True,null=True)
	pr_page = models.IntegerField(max_length=50)
	der_page = models.IntegerField(max_length=50)
	publisher = models.CharField(max_length=MAXCHAR)
	doi = models.CharField(max_length=MAXCHAR)
	theme = models.CharField(max_length=MAXCHAR,blank=True,null=True)
	date = models.DateField(null=True, blank=True)
	fichier = models.FileField(upload_to = get_file_path)
    



class Mot_cle(models.Model):
	formulaire = models.ForeignKey(Formulaire, on_delete = models.CASCADE)
	mot_cle = models.CharField(max_length=MAXCHAR,blank=True,null=True)


class Auteur(models.Model):
	PR_AUTEUR = 0
	CO_AUTEUR = 1

	TYPES = (
		(PR_AUTEUR, 'Premier Auteur'),
		(CO_AUTEUR, 'CO Auteur')
	)

	formulaire = models.ForeignKey(Formulaire, on_delete = models.CASCADE)
	auteur = models.CharField(max_length=MAXCHAR)
	auteur_type = models.IntegerField(choices= TYPES)





