from django.db import models

from Utils.const import *

from Account.models import UserAccount, RelationModel

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
	#pr_auteur = models.ForeignKey(AuteurModel, null=True, on_delete=models.SET_NULL)
	#co_auteur = models.TextField()
	user_publisher = models.ForeignKey(UserAccount, on_delete=models.SET_NULL, null=True, blank=True)
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
		auteurs = AuteurRelationsModel.objects.filter(auteur_type=1, pub=self)
		auteurs = [x.auteur.name for x in auteurs]
		s = re.sub(r"('|\[|\])", '', str(auteurs))
		s = re.sub(r",", ' , ', s)
		return s
	
	def getAuteur(self):
		return AuteurRelationsModel.objects.get(auteur_type=0, pub=self).auteur.name
	
	def getEncadrant(self):
		user = self.user_publisher
		if user.isDoctorant():
			encadrants = RelationModel.objects.filter(user1=user, relationType=0)
			if encadrants.exists():
				return encadrants[0].user2
		return None
	


class AuteurRelationsModel(models.Model):
	Types = (
		(0, "Pr.Auteur"),
		(1, "Co.Auteur"),
	)
	auteur = models.ForeignKey(AuteurModel, on_delete=models.CASCADE)
	pub = models.ForeignKey(PublicationModel, null=True, blank=True, on_delete=models.CASCADE)
	auteur_type = models.IntegerField(choices=Types, default=0)

	def __str__(self):
		return f'{self.pub}->{self.auteur}->{self.auteur_type}'



