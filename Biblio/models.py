from django.db import models

from Utils.const import *

from Account.models import UserAccount

import os
import json
import re

def get_file_path(self,filename):
	return f'files/{self.id}/{filename}'

class AuteurModel(models.Model):
	user = models.OneToOneField(UserAccount, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	# pub = models.ForeignKey(PublicationModel, null=True, blank=True, on_delete=models.CASCADE)
	# auteur_type = models.IntegerField(choices=Types, default=0)

	def __str__(self):
		return self.name

class PublicationModel(models.Model):
	#pr_auteur = models.CharField(max_length=MAXCHAR)
	pr_auteur = models.ForeignKey(AuteurModel, null=True, on_delete=models.SET_NULL)
	co_auteur = models.TextField()
	titre =models.CharField(max_length=MAXCHAR)
	type_pub = models.CharField(max_length=MAXCHAR)
	doi = models.CharField(max_length=MAXCHAR)
	volume = models.IntegerField(blank=True,null=True)
	pr_page = models.IntegerField()
	der_page = models.IntegerField()
	citation = models.IntegerField(blank=True,null=True)
	date = models.DateField(null=True, blank=True)
	journal = models.CharField(max_length=MAXCHAR)
	issn = models.CharField(max_length=ISSN_MAX)
	publisher = models.CharField(max_length=MAXCHAR,blank=True,null=True)
	fichier = models.FileField(upload_to = get_file_path)


	def __str__(self):
		return self.titre

	#getName sert a recuperer le nom du fichier

	def getName(self):
		return os.path.basename(self.fichier.name)

	#getLien sert a recuperer le lien de fichier

	def getLien(self):
		return f'/media/{self.fichier.name}'

	def get_coAuteur(self):
		co_auteur = json.loads(self.co_auteur)
		ids = [int(x['id']) for x in co_auteur]
		list_auteurs = AuteurModel.objects.filter(id__in = ids)
		co_auteur = [x.name + " #" + str(x.id) for x in list_auteurs]

		s = re.sub(r"('|\[|\])", '', str(co_auteur))
		s = re.sub(r",", ' , ', s)
		return s
	


# class AuteurRelationsModel(models.Model):
# 	Types = (
# 		(0, "Pr.Auteur"),
# 		(1, "Co.Auteur"),
# 	)
# 	auteur = models.ForeignKey(AuteurModel, on_delete=models.CASCADE)
# 	pub = models.ForeignKey(PublicationModel, null=True, blank=True, on_delete=models.CASCADE)
# 	auteur_type = models.IntegerField(choices=Types, default=0)



