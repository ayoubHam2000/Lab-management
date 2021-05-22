from django.db import models

class formulaire(models.Model):
    name=models.CharField(max_length=30)
    Email=models.EmailField(max_length=50)
    Filiere = models.CharField(max_length=20)
    photo = models.FileField(upload_to='')

    def getUrl(self):
        return f'/media/{self.photo.name}' 


    def __str__(self):
        return self.name


