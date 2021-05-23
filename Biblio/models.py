from django.db import models

class Formulaire(models.Model):
    name=models.CharField(max_length=30)
    email=models.EmailField(max_length=50)
    filiere = models.CharField(max_length=20)
    photo = models.FileField(upload_to='')

    def getUrl(self):
        return f'/media/{self.photo.name}' 


    def __str__(self):
        return self.name
