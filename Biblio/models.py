from django.db import models

from Utils.const import *

from Account.models import UserAccount, RelationModel

import os
import json
import re

def get_file_path(self,filename):
	return f'files/{self.id}/{filename}'


class PublicationModel(models.Model):
	pr_auteur = models.CharField(max_length=MAXCHAR)
	co_auteur = models.TextField()
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
		return self.co_auteur.replace(',', ' , ')
	
	def get_pr_author(self):
		return self.pr_auteur

	def getEncadrant(self):
		user = self.user_publisher
		if user.isDoctorant():
			encadrants = RelationModel.objects.filter(user1=user, relationType=0)
			if encadrants.exists():
				return encadrants[0].user2
		return None
	
	def getAllAuthors():
		auth = []
		pubs = PublicationModel.objects.all()
		for item in pubs:
			a = item.co_auteur.split(",") + [item.pr_auteur]
			for i in a:
				if i not in auth:
					auth.append(i)
		return auth
	





