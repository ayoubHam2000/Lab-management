from django.db import models

from Utils.const import *

from Account.models import UserAccount

import os

def get_file_path(self,filename):
	return f'files/{self.id}/{filename}'


class PublicationModel(models.Model):
	pr_auteur = models.CharField(max_length=MAXCHAR)
	co_auteur = models.CharField(max_length=10000)
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
		a = self.co_auteur
		return a.replace(",", " , ")

class Auteur(models.Model):
	Types = (
		(0, "Pr.Auteur"),
		(1, "Co.Auteur"),
	)
	user = models.ForeignKey(UserAccount, null=True, blank=True, on_delete=models.CASCADE)
	pub = models.ForeignKey(PublicationModel, on_delete=models.CASCADE)
	auteur_name = models.CharField(max_length=100)
	auteur_type = models.IntegerField(choices=Types, default=0)



