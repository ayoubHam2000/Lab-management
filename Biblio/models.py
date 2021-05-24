from django.db import models

from Utils.const import *

import os

def get_file_path(self,filename):
	return f'files/{self.id}/{filename}'

class Formulaire(models.Model):

	titre =models.CharField(max_length=MAXCHAR)
	type_pub = models.CharField(max_length=MAXCHAR)
	doi = models.CharField(max_length=MAXCHAR)
	pr_auteur = models.CharField(max_length=MAXCHAR)
	co_auteur = models.CharField(max_length=MAXCHAR)
	volume = models.IntegerField(max_length=VOLUME_MAX,blank=True,null=True)
	pr_page = models.IntegerField(max_length=50)
	der_page = models.IntegerField(max_length=50)
	date = models.DateField(null=True, blank=True)
	journal = models.CharField(max_length=MAXCHAR)
	issn = models.IntegerField(max_length=ISSN_MAX)
	publisher = models.CharField(max_length=MAXCHAR)
	fichier = models.FileField(upload_to = get_file_path)


	def __str__(self):
		return self.titre
	
	def getName(self):
		return os.path.basename(self.fichier.name)

	def getLien(self):
		return f'media/{self.fichier.name}'







